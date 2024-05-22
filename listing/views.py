from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from base.models import SiteImage

from .forms import ListingForm, ListingPostForm, ListingReviewForm, PropertyContactForm
from .models import (
    APPROVED,
    ListingAmenities,
    ListingCategory,
    ListingPost,
    ListingReview,
    ListingSubCategory,
)


def get_subcategories(request):
    category_id = request.GET.get("category")
    subcategories = ListingSubCategory.objects.filter(category_id=category_id).values(
        "id", "name"
    )
    return JsonResponse(list(subcategories), safe=False)


def get_all_subcategories(request):
    subcategories = ListingSubCategory.objects.all().values("id", "name")
    return JsonResponse(list(subcategories), safe=False)


def listing(request):
    listings = (
        ListingPost.objects.select_related("user")
        .prefetch_related(
            Prefetch("category", queryset=ListingCategory.objects.all()),
            Prefetch("subcategory", queryset=ListingSubCategory.objects.all()),
            Prefetch("amenities", queryset=ListingAmenities.objects.all()),
            Prefetch(
                "reviews", queryset=ListingReview.objects.select_related("user").all()
            ),
        )
        .filter(status=APPROVED)
        .all()
    )
    form = ListingForm(request.GET)
    if form.is_valid():
        print(form.cleaned_data)
        category_id = form.cleaned_data.get("business_category")
        if category_id is not None:
            form.fields["business_subcategory"].queryset = (
                ListingSubCategory.objects.filter(category_id=category_id)
            )
            listings = listings.filter(category=category_id)
        subcategory_id = form.cleaned_data.get("business_subcategory")
        if subcategory_id is not None:
            listings = listings.filter(subcategory=subcategory_id)
        business_name = form.cleaned_data.get("business_name")
        if business_name is not None:
            listings = listings.filter(Q(business_name__icontains=business_name))
        business_location = form.cleaned_data.get("business_location")
        if business_location is not None:
            listings = listings.filter(
                Q(location__icontains=business_location)
                | Q(street__icontains=business_location)
                | Q(city__icontains=business_location)
            )
        sorting = form.cleaned_data.get("business_sort")
        print("Sorting:" + sorting)

        # Recommended (Paid)
        if sorting in ["1", "0", ""]:
            pass
        # Newest (created at)
        elif sorting == "2":
            listings = listings.order_by("-created_at")
        # Most Reviewed
        elif sorting == "3":
            listings = listings.annotate(review_count=Count("reviews")).order_by(
                "-review_count"
            )
        # Top Rated (Top scoring )
        elif sorting == "4":
            listings = listings.annotate(
                average_rating=Avg("reviews__rating")
            ).order_by("-average_rating")
        # A to Z (Business Name)
        elif sorting == "5":
            listings = listings.order_by("business_name")

    paginator = Paginator(listings, 12)  # Show 10 listings per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "listing/listing.html",
        {"page_obj": page_obj, "listings": listings, "form": form},
    )


def category(request):
    return render(request, "listing/category.html")


def listing_details(request, listing_id):
    user_has_reviewed = False
    review_message = ""

    listing = (
        ListingPost.objects.select_related("user")
        .prefetch_related(
            Prefetch("category", queryset=ListingCategory.objects.all()),
            Prefetch("subcategory", queryset=ListingSubCategory.objects.all()),
            Prefetch("amenities", queryset=ListingAmenities.objects.all()),
            Prefetch(
                "reviews", queryset=ListingReview.objects.select_related("user").all()
            ),
        )
        .get(id=listing_id)
    )
    listings = (
        ListingPost.objects.select_related("user")
        .prefetch_related(
            Prefetch("category", queryset=ListingCategory.objects.all()),
            Prefetch("subcategory", queryset=ListingSubCategory.objects.all()),
            Prefetch("amenities", queryset=ListingAmenities.objects.all()),
            Prefetch(
                "reviews", queryset=ListingReview.objects.select_related("user").all()
            ),
        )
        .filter(subcategory__category=listing.subcategory.first().category)
        .exclude(id=listing_id)
        .all()[:5]
    )

    if request.user.is_authenticated:
        user_has_reviewed = ListingReview.objects.filter(
            user=request.user, listing=listing
        ).exists()
        if user_has_reviewed:
            review_message = "You have already reviewed this listing."

    reviews = ListingReview.objects.select_related("user").filter(
        listing__id=listing_id
    )
    review_form = ListingReviewForm(request.POST or None)
    contact_form = PropertyContactForm(request.POST or None)
    contact_form_success = False

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("account_login")

        if "review_submit" in request.POST:

            if review_form.is_valid():
                print(review_form.cleaned_data)
                review = review_form.save(commit=False)
                review.user = request.user
                review.listing = listing
                review.save()
                review_form = ListingReviewForm()
                review_message = "You have already reviewed this listing."

                return render(
                    request,
                    "listing/listing_details.html",
                    {
                        "listing": listing,
                        "listings": listings,
                        "reviews": reviews,
                        "review_message": review_message,
                        "contact_form": contact_form,
                        "contact_form_success": contact_form_success,
                        "review_success": "Thanks for your review.",
                    },
                )

        elif "contact_submit" in request.POST:
            if contact_form.is_valid():
                contact = contact_form.save(commit=False)
                contact.user = request.user
                contact.listing = listing
                contact.save()
                contact_form = PropertyContactForm()
                contact_form_success = True

    print(contact_form)
    print(review_form)
    return render(
        request,
        "listing/listing_details.html",
        {
            "listing": listing,
            "listings": listings,
            "reviews": reviews,
            "review_form": review_form if not user_has_reviewed else None,
            "review_message": review_message,
            "contact_form": contact_form,
            "contact_form_success": contact_form_success,
        },
    )


@login_required
def add_listing(request):
    hero_image = SiteImage.objects.filter(place="add_listing").first()

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data["user"] = request.user
        form = ListingPostForm(post_data, request.FILES)
        if form.is_valid():
            form.save()
            form = ListingPostForm()
            return render(
                request,
                "listing/add_listing.html",
                {
                    "form": form,
                    "hero_image": hero_image,
                    "success": "Listing added successfully. Please wait for the admin to approve.",
                },
            )
    else:
        form = ListingPostForm()

    return render(
        request, "listing/add_listing.html", {"form": form, "hero_image": hero_image}
    )
