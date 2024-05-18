from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from PIL import Image

APPROVED = "A"
PENDING = "P"
DENIED = "D"
PAID = "P"
FREE = "F"

LISTING_IMAGE_SIZE = (670, 390)

STATUS_CHOICES = [
    (APPROVED, "Approved"),
    (PENDING, "Pending"),
    (DENIED, "Denied"),
]


class ListingAmenities(models.Model):
    title = models.CharField(max_length=1000, help_text="Enter the amenities title")
    description = models.CharField(
        max_length=2000, help_text="Enter the amenities description"
    )
    image = models.ImageField(
        upload_to="amenities/images", help_text="Upload the amenities image(80*80)"
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        verbose_name_plural = "Property Amenties"
        ordering = ("title",)


class ListingCategory(models.Model):
    name = models.CharField(max_length=1000, help_text="Enter the category name")
    logo = models.ImageField(
        upload_to="listing/images/",
        help_text="Upload the category logo(80*80)",
        verbose_name="Category Logo",
    )
    on_home = models.BooleanField(
        default=False,
        help_text="Show this category on hero section of home page",
        verbose_name="Show on homepage",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

    def total_listing(self):
        return self.category_listing.filter(status=APPROVED).count()

    class Meta:
        verbose_name_plural = "Property Categories"
        ordering = ("name",)


class ListingSubCategory(models.Model):
    category = models.ForeignKey(
        ListingCategory,
        on_delete=models.CASCADE,
        related_name="subcategory",
        help_text="Select the category",
    )
    name = models.CharField(max_length=1000, help_text="Enter the subcategory name")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

    def total_listing(self):
        return self.subcategory_listing.count()

    class Meta:
        verbose_name_plural = "Property SubCategories"
        ordering = ("name",)


class ListingPost(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Author who submitted the listing"
    )
    business_name = models.CharField(
        max_length=1000, help_text="Enter the property name"
    )
    category = models.ForeignKey(
        ListingCategory,
        related_name="category_listing",
        help_text="Select the property category",
        blank=True,
        on_delete=models.CASCADE,
    )
    subcategory = models.ManyToManyField(
        ListingSubCategory,
        related_name="subcategory_listing",
        help_text="Select the property subcategories",
        verbose_name="Categories & Subcategories",
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text="Choose whether to display on site or not",
        blank=True,
        null=True,
    )
    on_home = models.BooleanField(
        default=False,
        help_text="Show this post on hero section of home page",
        verbose_name="Show on homepage",
    )

    description = models.TextField(help_text="Enter the property description")
    location = models.CharField(
        max_length=1000,
        help_text=" Enter the location (building, tool, chowk etc) ",
        blank=True,
        null=True,
    )
    street = models.CharField(
        max_length=1000,
        help_text=" Enter the street address (street name, area etc)",
    )

    city = models.CharField(
        max_length=1000,
        help_text=" Enter the city name",
    )

    state = models.CharField(
        max_length=1000, help_text="Enter the province name", blank=True, null=True
    )

    latitude = models.CharField(
        max_length=15,
        help_text="Enter the latitude",
        blank=True,
        null=True,
    )

    longitude = models.CharField(
        max_length=15,
        help_text="Enter the longitude",
        blank=True,
        null=True,
    )

    email = models.EmailField(help_text="Enter the email")

    main_phone = models.CharField(
        max_length=20,
        help_text="Enter the phone number",
        verbose_name="Phone Number",
    )
    mobile_phone = models.CharField(
        max_length=20,
        help_text="Enter the mobile phone number",
        blank=True,
        null=True,
    )

    image1 = models.ImageField(
        upload_to="listing/images/", help_text="Upload the listing image(670*390)"
    )
    image2 = models.ImageField(
        upload_to="listing/images/",
        help_text="Upload the listing image(670*390)",
        blank=True,
        null=True,
    )
    image3 = models.ImageField(
        upload_to="listing/images/",
        help_text="Upload the listing image(670*390)",
        blank=True,
        null=True,
    )
    image4 = models.ImageField(
        upload_to="listing/images/",
        help_text="Upload the listing image(670*390)(Available for only paid listing)",
        blank=True,
        null=True,
    )
    image5 = models.ImageField(
        upload_to="listing/images/",
        help_text="Upload the listing image(670*390)(Available for only paid listing)",
        blank=True,
        null=True,
    )
    image6 = models.ImageField(
        upload_to="listing/images/",
        help_text="Upload the listing image(670*390)(Available for only paid listing)",
        blank=True,
        null=True,
    )

    amenities = models.ManyToManyField(
        ListingAmenities,
        help_text="Select the property amenities",
        blank=True,
    )
    price = models.CharField(help_text="Enter the listing high price", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image_fields = [
            self.image1,
            self.image2,
            self.image3,
            self.image4,
            self.image5,
            self.image6,
        ]
        for image_field in image_fields:
            if image_field:
                img = Image.open(image_field.path)
                width, height = img.size
                aspect = width / float(height)

                ideal_width, ideal_height = LISTING_IMAGE_SIZE
                ideal_aspect = ideal_width / float(ideal_height)

                if aspect > ideal_aspect:
                    # Then crop the left and right edges:
                    new_width = int(ideal_aspect * height)
                    offset = (width - new_width) / 2
                    resize = (offset, 0, width - offset, height)
                else:
                    # ... crop the top and bottom:
                    new_height = int(width / ideal_aspect)
                    offset = (height - new_height) / 2
                    resize = (0, offset, width, height - offset)

                img = img.crop(resize).resize(
                    (ideal_width, ideal_height), Image.Resampling.LANCZOS
                )
                img.save(image_field.path)

    def average_rating(self):
        """Return average rating of a product"""
        return (
            self.reviews.filter(status=APPROVED)
            .aggregate(rating=Avg("rating"))
            .get("rating")
        )

    def __str__(self) -> str:
        return str(self.business_name)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ("-created_at",)


class PropertyContact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Author who created the review"
    )
    listing = models.ForeignKey(
        ListingPost,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Select the property",
    )
    subject = models.CharField(max_length=255, help_text="Subject of the message")
    message = models.TextField(help_text="Contact Description")
    submit_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.subject)

    class Meta:
        verbose_name_plural = "Properties Contacts"
        ordering = ("-submit_date",)


class ListingReview(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Author who created the review"
    )
    listing = models.ForeignKey(
        ListingPost,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Select the property",
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text="Choose whether to display on site or not",
    )
    title = models.CharField(help_text="Enter the title of your review", max_length=500)
    description = models.TextField(help_text="Enter the description of the review")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Enter the rating of the listing between 1 and 5",
    )

    def __str__(self) -> str:
        return f"{str(self.listing)}_{str(self.user)}"

    class Meta:
        verbose_name_plural = "Property Reviews"
        unique_together = ("user", "listing")
        ordering = ("-created_at",)
