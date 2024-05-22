from django.db.models import Count

from listing.models import ListingCategory

from .models import About, SiteImage


def add_global_context(request):
    context_about = About.objects.first()
    context_profile_image = SiteImage.objects.filter(place="profile_hero").first()
    context_category = ListingCategory.objects.annotate(
        num_listings=Count("category_listing")
    ).order_by("-num_listings")[:5]
    context_ad_image = SiteImage.objects.filter(place="ad").first()

    return {
        "context_about": context_about,
        "context_category": context_category,
        "context_ad_image": context_ad_image,
        "context_profile_image": context_profile_image,
        "context_pages": None,
    }
