# from django import forms
from django.contrib import admin
from django.db import models as django_models
from django.db.models import Prefetch
from tinymce.widgets import TinyMCE
from unfold import forms
from unfold.admin import ModelAdmin
from unfold.decorators import display

from . import models


@admin.register(models.ListingAmenities)
class ListingAmenitiesAdmin(ModelAdmin):
    list_display = ["title", "created_at", "updated_at"]
    list_per_page = 10
    search_fields = ["title"]


@admin.register(models.ListingCategory)
class ListingCategoryAdmin(ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    list_per_page = 10
    search_fields = ["name"]
    list_filter = ["on_home"]


@admin.register(models.ListingSubCategory)
class ListingSubCategoryAdmin(ModelAdmin):
    list_display = ["name", "category", "updated_at"]
    list_per_page = 10
    search_fields = ["name"]


class GroupedSelectMultiple(forms.forms.SelectMultiple):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option_dict = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if subindex is None:
            option_dict["attrs"]["class"] = "optiongroup"
        option_dict["attrs"]["style"] = "width: 250px"
        return option_dict


@admin.register(models.ListingPost)
class ListingPostAdmin(ModelAdmin):
    list_display = [
        "business_name",
        "created_at",
        "show_status",
    ]
    list_per_page = 10
    search_fields = ["business_name", "subcategory__name"]
    readonly_fields = ["user"]
    list_filter = ["status", "on_home"]
    exclude = ["category"]

    @display(
        description="Status",
        ordering="status",
        label={
            "Approved": "success",
            "Pending": "info",
            "Denied": "danger",
        },
    )
    def show_status(self, obj):
        return obj.get_status_display()

    def get_grouped_choices(self):
        categories = models.ListingCategory.objects.prefetch_related(
            Prefetch("subcategory", queryset=models.ListingSubCategory.objects.all())
        )
        grouped_choices = []
        for category in categories:
            subcategories = category.subcategory.all()
            subcategory_choices = [
                (subcategory.id, subcategory.name) for subcategory in subcategories
            ]
            grouped_choices.append((category.name, subcategory_choices))
        return grouped_choices

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "subcategory":
            kwargs["widget"] = GroupedSelectMultiple
            return db_field.formfield(**kwargs)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if not obj.user_id:
                obj.user_id = request.user.id
        new_subcategory = form.cleaned_data.get("subcategory").first()
        obj.category = new_subcategory.category
        super().save_model(request, obj, form, change)

    formfield_overrides = {
        django_models.TextField: {
            "widget": TinyMCE,
        }
    }


@admin.register(models.ListingReview)
class ListingReviewAdmin(ModelAdmin):
    list_display = [
        "listing",
        "user",
        "rating",
        "created_at",
        "show_status",
    ]
    list_per_page = 10
    search_fields = ["business_name", "category__name", "subcategory__name"]
    readonly_fields = ["user"]
    list_filter = ["status"]

    @display(
        description="Status",
        ordering="status",
        label={
            "Approved": "success",  # green
            "Pending": "info",  # blue
            "Denied": "danger",  # red
        },
    )
    def show_status(self, obj):
        return obj.get_status_display()

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Object is being created, not updated
            if not obj.user_id:  # User field is not populated
                obj.user_id = request.user.id
        super().save_model(request, obj, form, change)


@admin.register(models.PropertyContact)
class PropertyContactAdmin(ModelAdmin):
    list_display = ["subject", "listing", "user"]
    list_per_page = 10
    search_fields = ["subject"]
