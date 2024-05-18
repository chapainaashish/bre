from django.contrib import admin, messages
from django.db import models as django_models
from django.shortcuts import redirect
from django.urls import reverse
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from . import models


@admin.register(models.SiteImage)
class SiteImageAdmin(ModelAdmin):
    list_display = ["place", "created_at", "updated_at"]
    list_per_page = 10
    search_fields = ["place"]


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "submit_date"]
    list_per_page = 10
    search_fields = ["subject"]

    def has_add_permission(self, request):
        return False


@admin.register(models.Faq)
class FaqAdmin(ModelAdmin):
    list_display = ["question", "created_at"]
    list_per_page = 10
    search_fields = ["question", "answer"]


@admin.register(models.About)
class AboutAdmin(ModelAdmin):
    list_display = ["about_title", "created_at", "updated_at"]
    list_per_page = 10
    search_fields = ["about_title", "about_text"]

    formfield_overrides = {
        django_models.TextField: {
            "widget": TinyMCE,
        }
    }

    def add_view(self, request, form_url="", extra_context=None):
        if models.About.objects.exists():
            obj = models.About.objects.first()
            messages.error(
                request,
                "An instance of About already exists. You can't have two about.",
            )
            return redirect(reverse("admin:base_about_change", args=(obj.pk,)))
        return super().add_view(request, form_url, extra_context)


@admin.register(models.Page)
class PageAdmin(ModelAdmin):
    list_display = ["title", "created_at", "updated_at"]
    list_per_page = 10
    search_fields = ["title"]
    exclude = ["slug"]

    formfield_overrides = {
        django_models.TextField: {
            "widget": TinyMCE,
        }
    }
