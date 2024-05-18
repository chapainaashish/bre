from django.contrib import admin
from django.db import models as django_models
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from . import models


@admin.register(models.BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    list_per_page = 10
    search_fields = ["name"]


@admin.register(models.BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ["title", "category", "created_at"]
    list_per_page = 10
    search_fields = ["name"]

    formfield_overrides = {
        django_models.TextField: {
            "widget": TinyMCE,
        }
    }
