from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "first_name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "last_name"}),
    )

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "image",
            "bio",
            "phone",
            "website",
            "facebook",
            "twitter",
            "linkedin",
            "skype",
            "pinterest",
            "google_plus",
        ]
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "form-control img-upload-box", "id": "img-upload2"}
            ),
            "bio": forms.Textarea(
                attrs={"class": "form-control", "id": "description", "rows": "3"}
            ),
            "phone": forms.TextInput(attrs={"class": "form-control", "id": "phone"}),
            "website": forms.URLInput(attrs={"class": "form-control", "id": "website"}),
            "facebook": forms.URLInput(
                attrs={"class": "form-control", "id": "facebook"}
            ),
            "twitter": forms.URLInput(attrs={"class": "form-control", "id": "twitter"}),
            "linkedin": forms.URLInput(
                attrs={"class": "form-control", "id": "linkedin"}
            ),
            "skype": forms.TextInput(attrs={"class": "form-control", "id": "skype"}),
            "pinterest": forms.URLInput(
                attrs={"class": "form-control", "id": "pinterest"}
            ),
            "google_plus": forms.URLInput(
                attrs={"class": "form-control", "id": "google_plus"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
