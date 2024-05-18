from django import forms
from django.forms import EmailInput, ModelForm, Textarea, TextInput

from listing.models import ListingCategory

from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "subject", "description")

        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your name",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email",
                }
            ),
            "subject": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the subject",
                }
            ),
            "description": Textarea(
                attrs={
                    "rows": "6",
                    "class": "form-control",
                    "placeholder": "Enter the description",
                }
            ),
        }


class HeroForm(forms.Form):
    business_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter property name...",
                "id": "form-website",
                "required": "",
                "data-error": "Search text required",
                "style": "height: 60px; font-size:16px;",
            }
        ),
    )

    business_category = forms.ModelChoiceField(
        queryset=ListingCategory.objects.all(),
        required=False,
        empty_label="Choose property category",
        widget=forms.Select(
            attrs={
                "class": "select2 form-control",
                "id": "category",
                "placeholder": "All Categories",
            }
        ),
    )


class FAQSearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search FAQ...",
                "style": "height: 50px; font-size: 15px; padding:15px;",
            }
        )
    )
