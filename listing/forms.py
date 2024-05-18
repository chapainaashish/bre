from django import forms
from tinymce.widgets import TinyMCE

from .models import (
    ListingCategory,
    ListingPost,
    ListingReview,
    ListingSubCategory,
    PropertyContact,
)


class ListingForm(forms.Form):
    SORT_CHOICES = [
        ("0", "Sort By"),
        ("1", "Recommended"),
        ("2", "Newest"),
        ("3", "Most Reviewed"),
        ("4", "Top Rated"),
        ("5", "A to Z"),
    ]

    business_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter properties name...",
            }
        ),
    )
    business_location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter location, street, area or city...",
            }
        ),
    )
    business_category = forms.ModelChoiceField(
        queryset=ListingCategory.objects.all(),
        required=False,
        empty_label="Choose Category",
        widget=forms.Select(attrs={"class": "select2"}),
    )
    business_subcategory = forms.ModelChoiceField(
        queryset=ListingSubCategory.objects.all(),
        required=False,
        empty_label="Choose Subcategory",
        widget=forms.Select(attrs={"class": "select2"}),
    )
    business_sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "select2"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        category_id = cleaned_data.get("business_category")
        subcategory_id = cleaned_data.get("business_subcategory")

        if category_id is None:
            if "business_category" in self._errors:
                del self._errors["business_category"]

        if subcategory_id is None:
            if "business_subcategory" in self._errors:
                del self._errors["business_subcategory"]

        return cleaned_data


class ListingReviewForm(forms.ModelForm):
    class Meta:
        model = ListingReview
        fields = ["title", "description", "rating"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "", "required": True}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea form-control",
                    "cols": 20,
                    "rows": 7,
                    "required": True,
                }
            ),
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "required": True}
            ),
        }


class ContactPropertyForm(forms.Form):
    class Meta:
        model = PropertyContact
        fields = ["subject", "message"]

        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "",
                    "data-error": "Subject field is required",
                },
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "textarea form-control",
                    "cols": "20",
                    "rows": "7",
                    "placeholder": "",
                    "data-error": "Message field is required",
                }
            ),
        }


class ListingPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListingPostForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
        self.fields["image2"].required = False
        self.fields["image3"].required = False
        self.fields["image4"].required = False
        self.fields["image5"].required = False
        self.fields["image6"].required = False
        self.fields["amenities"].required = False
        self.fields["status"].required = False

    class Meta:
        model = ListingPost
        fields = "__all__"
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "business_name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                    "style": "padding: 0 10px; height:50px;",
                }
            ),
            "subcategory": forms.SelectMultiple(attrs={"class": "form-control"}),
            "description": TinyMCE(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "street": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "latitude": forms.TextInput(attrs={"class": "form-control"}),
            "longitude": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "main_phone": forms.TextInput(attrs={"class": "form-control"}),
            "mobile_phone": forms.TextInput(attrs={"class": "form-control"}),
            "image1": forms.FileInput(
                attrs={"class": "form-control img-upload-box", "id": "img-upload1"}
            ),
            "image2": forms.FileInput(
                attrs={"class": "form-control img-upload-box", "id": "img-upload2"}
            ),
            "image3": forms.FileInput(
                attrs={"class": "form-control img-upload-box", "id": "img-upload3"}
            ),
            "amenities": forms.SelectMultiple(attrs={"class": "form-control"}),
            "price": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter the price"}
            ),
        }
