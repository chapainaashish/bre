from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, render

from blog.models import BlogPost
from listing.models import (
    APPROVED,
    ListingAmenities,
    ListingCategory,
    ListingPost,
    ListingReview,
    ListingSubCategory,
)

from .forms import ContactForm, FAQSearchForm, HeroForm
from .models import About, Faq, SiteImage


def home(request):
    heroform = HeroForm(request.GET)

    categories = ListingCategory.objects.annotate(
        num_listings=Count("category_listing")
    ).order_by("-num_listings")[:15]

    pin_categories = ListingCategory.objects.all()

    pin_listings = (
        ListingPost.objects.select_related("user")
        .prefetch_related(
            Prefetch("category", queryset=ListingCategory.objects.all()),
            Prefetch("subcategory", queryset=ListingSubCategory.objects.all()),
            Prefetch("amenities", queryset=ListingAmenities.objects.all()),
            Prefetch(
                "reviews", queryset=ListingReview.objects.select_related("user").all()
            ),
        )
        .order_by("-updated_at")
        .all()[:4]
    )

    blogs = (
        BlogPost.objects.select_related("category").order_by("-created_at").all()[:2]
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
        .order_by("-created_at")
        .all()[:6]
    )
    home_hero_image = SiteImage.objects.get(place="home_hero")
    home_main_image = SiteImage.objects.get(place="home_main")

    context = {
        "blogs": blogs,
        "heroform": heroform,
        "listings": listings,
        "home_hero_image": home_hero_image,
        "home_main_image": home_main_image,
        "pin_listings": pin_listings,
        "pin_categories": pin_categories,
        "categories": categories,
    }

    return render(request, "base/home.html", context=context)


def contact(request):
    longitude = latitude = 3
    contact_image = SiteImage.objects.get(place="contact")
    about = About.objects.all().first()
    if about is not None and about.longitude and about.latitude:
        longitude = about.longitude
        latitude = about.latitude

    if request.method == "POST":
        form = ContactForm(request.POST)
        empty_form = ContactForm()
        if form.is_valid():
            form.save()
            return render(
                request,
                "base/contact.html",
                {
                    "success": "Thanks for contacting us",
                    "form": empty_form,
                    "contact_image": contact_image,
                    "longitude": longitude,
                    "latitude": latitude,
                },
            )
        else:
            return render(
                request,
                "base/contact.html",
                {
                    "error": "Please review your form",
                    "form": form,
                    "contact_image": contact_image,
                    "longitude": longitude,
                    "latitude": latitude,
                },
            )
    else:
        form = ContactForm()
        return render(
            request,
            "base/contact.html",
            context={
                "form": form,
                "contact_image": contact_image,
                "longitude": longitude,
                "latitude": latitude,
            },
        )


def about(request):
    return render(request, "base/about.html")


def faq(request):
    faqs = Faq.objects.all().order_by("-created_at")
    faq_image = SiteImage.objects.get(place="faq")
    form = FAQSearchForm(request.GET)
    if form.is_valid():
        search_term = form.cleaned_data["search"]
        faqs = faqs.filter(question__icontains=search_term) | faqs.filter(
            answer__icontains=search_term
        )
    return render(
        request, "base/faq.html", {"faqs": faqs, "faq_image": faq_image, "form": form}
    )


def error_404(request):
    return render(request, "base/error_404.html")
