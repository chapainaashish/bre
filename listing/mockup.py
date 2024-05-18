import os

from django.contrib.auth.models import User
from django.core.files import File

from .models import ListingAmenities, ListingCategory, ListingPost, ListingSubCategory


def create_mockup_data():
    # Create a user
    user = User.objects.create_user(username="testuser", password="12345")

    # Create a ListingCategory
    category = ListingCategory.objects.create(
        name="TestCategory", logo=File(open("./logo.jpg", "rb"))
    )

    # Create a ListingSubCategory
    subcategory = ListingSubCategory.objects.create(
        name="TestSubCategory", category=category
    )

    # Create a ListingAmenities
    amenity = ListingAmenities.objects.create(
        title="TestAmenity",
        description="TestAmenity",
        image=File(open("./logo.jpg", "rb")),
    )

    # Create 100 ListingPost objects
    for i in range(100):
        listing = ListingPost.objects.create(
            user=user,
            business_name=f"TestBusiness{i}",
            status="A",
            plan="P",
            description="TestDescription",
            keywords="TestKeywords",
            location="TestLocation",
            street="TestStreet",
            city="TestCity",
            state="TestState",
            postal=12345,
            country="TestCountry",
            latitude="0.0",
            longitude="0.0",
            name="TestName",
            email="test@test.com",
            main_phone="1234567890",
            website="http://test.com",
            image1=File(open("./logo.jpg", "rb")),
            pricing_title="TestPricingTitle",
            low_price="0",
            high_price="100",
        )
        listing.category.add(category)
        listing.subcategory.add(subcategory)
        listing.amenities.add(amenity)
