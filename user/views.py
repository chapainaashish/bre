from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from listing.models import ListingPost

from .forms import ProfileForm
from .models import Profile


def register(request):
    return render(request, "user/register.html")


@login_required
def profile(request):
    profile_image_url = request.build_absolute_uri(request.user.profile.image.url)
    listings = ListingPost.objects.filter(user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            user=request.user,
            instance=request.user.profile,
        )
        if form.is_valid():
            profile = form.save(commit=False)
            request.user.first_name = form.cleaned_data.get("first_name")
            request.user.last_name = form.cleaned_data.get("last_name")
            request.user.save()
            profile.save()

    else:
        form = ProfileForm(user=request.user, instance=request.user.profile)

    paginator = Paginator(listings, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "user/profile.html",
        {
            "form": form,
            "profile_image_url": profile_image_url,
            "page_obj": page_obj,
        },
    )
