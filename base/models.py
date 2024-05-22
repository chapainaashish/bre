from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class SiteImage(models.Model):
    PLACE = [
        ("faq", "FAQ Hero Image (1920*251)"),
        ("contact", "Contact Hero Image (1920*251)"),
        ("blog", "Blog Hero Image(1920*251)"),
        ("ad", "Ad Image(359*560)"),
        ("home_hero", "Home Hero Image(1920*890)"),
        ("home_main", "Home Main Image(1920*960)"),
        ("profile_hero", "Profile Hero Image(1920*251)"),
        ("add_listing", "Add Listing Hero Image(1920*251)"),
    ]
    place = models.CharField(
        max_length=20,
        choices=PLACE,
        unique=True,
        error_messages={
            "unique": "An image for this place already exists. You can't add two images in one place",
        },
        help_text="Choose the image placement",
    )
    image = models.ImageField(
        upload_to="decoration/images",
        help_text="Upload the image",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.place

    class Meta:
        verbose_name_plural = "Site Images"


class Faq(models.Model):
    question = models.TextField(help_text="Enter the FAQ question")
    answer = models.TextField(help_text="Enter the FAQ answer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.question

    class Meta:
        verbose_name_plural = "FAQs"


class About(models.Model):
    hero_image = models.ImageField(
        upload_to="about/images", help_text="Upload the about hero image (1921*251)"
    )
    side_image = models.ImageField(
        upload_to="about/images", help_text="Upload the about side image (690*767)"
    )
    footer_image = models.ImageField(
        upload_to="about/images", help_text="Upload the about footer image (1920*541)"
    )
    about_title = models.CharField(help_text="Enter the about title", max_length=500)
    about_text = models.TextField(
        help_text="Enter the about description", verbose_name="About description"
    )
    location = models.CharField(help_text="Enter the location", max_length=500)
    latitude = models.CharField(
        max_length=100,
        help_text="Enter the latitude",
        blank=True,
        null=True,
    )

    longitude = models.CharField(
        max_length=100,
        help_text="Enter the longitude",
        blank=True,
        null=True,
    )
    email = models.EmailField(help_text="Enter the email")
    phone = models.CharField(max_length=20, help_text="Enter the phone number")
    facebook = models.URLField(
        help_text="Enter the Facebook URL", blank=True, null=True
    )
    instagram = models.URLField(
        help_text="Enter the Instagram URL", blank=True, null=True
    )
    twitter = models.URLField(
        help_text="Enter the X (Formerly Twitter) URL",
        verbose_name="X (Formerly Twitter)",
        blank=True,
        null=True,
    )
    linkedin = models.URLField(
        help_text="Enter the LinkedIn URL", blank=True, null=True
    )
    dribble = models.CharField(
        help_text="Enter the Dribble URL", blank=True, null=True, max_length=500
    )
    rss = models.CharField(
        help_text="Enter the RSS URL", blank=True, null=True, max_length=500
    )
    vk = models.CharField(
        help_text="Enter the VK URL", blank=True, null=True, max_length=500
    )
    linkedin = models.URLField(
        help_text="Enter the LinkedIn URL", blank=True, null=True
    )
    skype = models.CharField(
        max_length=1000,
        help_text="Enter the Skype ID",
        blank=True,
        null=True,
    )
    google_plus = models.CharField(
        help_text="Enter the Google Plus URL",
        blank=True,
        null=True,
        max_length=500,
    )
    pinterest = models.URLField(
        help_text="Enter the Pinterest URL",
        blank=True,
        null=True,
    )
    about_youtube_url = models.URLField(
        help_text="Enter the Youtube Video URL that you want to show in about section",
        blank=True,
        null=True,
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not About.objects.filter(pk=self.pk).exists() and About.objects.exists():
            raise ValidationError("There can be only one instance of this model")
        return super(About, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str("About us")

    class Meta:
        verbose_name_plural = "About"


# for contact us
class Contact(models.Model):
    name = models.CharField(max_length=1000, help_text="Contact Person Name")
    email = models.EmailField(help_text="Contact Email Address")
    subject = models.CharField(max_length=255, help_text="Subject of the message")
    description = models.TextField(help_text="Contact Description")
    submit_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str("Contact us")
