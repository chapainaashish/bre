from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, help_text="User associated with this profile"
    )
    image = models.ImageField(
        upload_to="user/cover",
        help_text="User Profile Picture",
        default="user/cover/default_user.png",
        blank=True,
        null=True,
    )
    bio = models.TextField(
        max_length=100,
        help_text="User description or bio",
    )
    phone = models.CharField(
        max_length=40, help_text="User phone number", blank=True, null=True
    )
    website = models.URLField(help_text="Enter the website URL", blank=True, null=True)
    designation = models.CharField(
        max_length=1000, help_text="Enter the designation", blank=True, null=True
    )
    company = models.CharField(
        max_length=1000, help_text="Enter the company name", blank=True, null=True
    )
    facebook = models.URLField(
        help_text="Enter the Facebook URL", blank=True, null=True
    )
    twitter = models.URLField(help_text="Enter the Twitter URL", blank=True, null=True)
    linkedin = models.URLField(
        help_text="Enter the LinkedIn URL", blank=True, null=True
    )
    skype = models.CharField(
        max_length=1000, help_text="Enter the Skype ID", blank=True, null=True
    )
    google_plus = models.URLField(
        help_text="Enter the Google Plus URL", blank=True, null=True
    )
    pinterest = models.URLField(
        help_text="Enter the Pinterest URL", blank=True, null=True
    )

    def __str__(self) -> str:
        return self.user.username
