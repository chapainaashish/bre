import os
from pathlib import Path

from django.templatetags.static import static
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-jwv0o!=p%0&uc1*jpp44*&d)pgww@t81b$@+@+*jz(q%&!%aa7"
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "unfold",
    "tinymce",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin_auto_filters",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "widget_tweaks",
    "base",
    "listing",
    "blog",
    "user",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "listygo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR.joinpath("templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "base.context_processor.add_global_context",
            ],
        },
    },
]

WSGI_APPLICATION = "listygo.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "property",
        "USER": "admin",
        "PASSWORD": "71904638930",
        "HOST": "localhost",
        "PORT": "3306",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


UNFOLD = {
    "SITE_TITLE": "Birauta Real Estate and Housing Pvt Ltd",
    "SITE_HEADER": "Birauta Real Estate and Housing Pvt Ltd",
    "SITE_ICON": lambda request: static("base/img/favicon.png"),
    "COLORS": {
        "primary": {
            "50": "255 235 238",
            "100": "255 205 210",
            "200": "239 154 154",
            "300": "229 115 115",
            "400": "239 83 80",
            "500": "244 67 54",
            "600": "229 57 53",
            "700": "211 47 47",
            "800": "198 40 40",
            "900": "183 28 28",
            "950": "78 1 1",
        },
    },
    "SITE_SYMBOL": "map",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Authentication and Authorization",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "auth.view_user"
                        ),
                    },
                    {
                        "title": "Profiles",
                        "icon": "account_circle",
                        "link": reverse_lazy("admin:user_profile_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "user.view_profile"
                        ),
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "auth.view_group"
                        ),
                    },
                ],
            },
            {
                "title": "Listing",
                "separator": True,
                "items": [
                    {
                        "title": "Properties",
                        "icon": "post",
                        "link": reverse_lazy("admin:listing_listingpost_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "listing.view_listingpost"
                        ),
                    },
                    {
                        "title": "Property Queries",
                        "icon": "perm_phone_msg",  # Choose an appropriate icon
                        "link": reverse_lazy(
                            "admin:listing_propertycontact_changelist"
                        ),
                        "permission": lambda request: request.user.has_perm(
                            "listing.view_propertycontact"
                        ),
                    },
                    {
                        "title": "Property Reviews",
                        "icon": "star_half",  # Choose an appropriate icon
                        "link": reverse_lazy("admin:listing_listingreview_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "listing.view_listingreview"
                        ),
                    },
                    {
                        "title": "Property Categories",
                        "icon": "category",
                        "link": reverse_lazy(
                            "admin:listing_listingcategory_changelist"
                        ),
                        "permission": lambda request: request.user.has_perm(
                            "listing.view_listingcategory"
                        ),
                    },
                    {
                        "title": "Property SubCategories",
                        "icon": "category",
                        "link": reverse_lazy(
                            "admin:listing_listingsubcategory_changelist"
                        ),
                        "permission": lambda request: request.user.has_perm(
                            "listing.view_listingsubcategory"
                        ),
                    },
                    {
                        "title": "Property Amenities",
                        "icon": "roofing",
                        "link": reverse_lazy(
                            "admin:listing_listingamenities_changelist"
                        ),
                        "permission": lambda request: request.user.has_perm(
                            "listing.view_listingamenities"
                        ),
                    },
                ],
            },
            {
                "title": "Blog",
                "separator": True,
                "items": [
                    {
                        "title": "Blog Categories",
                        "icon": "category",
                        "link": reverse_lazy("admin:blog_blogcategory_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "blog.view_blogcategory"
                        ),
                    },
                    {
                        "title": "Blog Posts",
                        "icon": "post",
                        "link": reverse_lazy("admin:blog_blogpost_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "blog.view_blogpost"
                        ),
                    },
                ],
            },
            {
                "title": "Base Content",
                "separator": True,
                "items": [
                    {
                        "title": "Site Images",
                        "icon": "image",
                        "link": reverse_lazy("admin:base_siteimage_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "base.view_siteimages"
                        ),
                    },
                    {
                        "title": "About",
                        "icon": "info",
                        "link": reverse_lazy("admin:base_about_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "base.view_about"
                        ),
                    },
                    {
                        "title": "Contacts",
                        "icon": "contacts",
                        "link": reverse_lazy("admin:base_contact_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "base.view_contact"
                        ),
                    },
                    {
                        "title": "FAQs",
                        "icon": "help",
                        "link": reverse_lazy("admin:base_faq_changelist"),
                        "permission": lambda request: request.user.has_perm(
                            "base.view_faq"
                        ),
                    },
                ],
            },
        ],
    },
}


CSRF_TRUSTED_ORIGINS = [
    "https://digitaline.com",
    "https://www.digitaline.com",
    "http://digitaline.com",
    "http://www.digitaline.com",
]

TINYMCE_DEFAULT_CONFIG = {
    "height": 656,
    "plugins": [
        "advlist autolink link image lists charmap print preview hr anchor pagebreak",
        "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
        "table emoticons template paste help",
        "codesample",
        "link",
        "image",
        "code",
        "table",
        "lists",
        "media",
    ],
    "toolbar": "undo redo | formatselect | bold italic underline strikethrough | "
    + "fontselect fontsizeselect | alignleft aligncenter alignright alignjustify | "
    + "outdent indent | numlist bullist checklist | forecolor backcolor removeformat | "
    + "pagebreak | charmap emoticons | fullscreen preview save print | insertfile image media template link anchor codesample | "
    + "link image code table lists media | help",
    "menubar": "file edit view insert format tools table help",
    "toolbar_drawer": "floating",
    "tinycomments_mode": "embedded",
    "tinycomments_author": "Author name",
}


ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "profile"
LOGIN_URL = "account_login"
ACCOUNT_LOGOUT_REDIRECT_URL = "account_login"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
