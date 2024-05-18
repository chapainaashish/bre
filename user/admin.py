from django.contrib import admin
from unfold.admin import ModelAdmin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(ModelAdmin):
    list_display = [
        "user",
        "phone",
        "user_date_joined",
        "user_last_login",
    ]

    def user_last_login(self, obj):
        return obj.user.last_login

    user_last_login.short_description = "Last Login"

    def user_date_joined(self, obj):
        return obj.user.date_joined

    user_date_joined.short_description = "Date Joined"
