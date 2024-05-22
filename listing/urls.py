from django.urls import path

from . import views

urlpatterns = [
    path("", views.listing, name="listing"),
    path("<int:listing_id>/", views.listing_details, name="listing_details"),
    path("category/", views.category, name="category"),
    path("add/", views.add_listing, name="add_listing"),
    path("edit/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("delete/<int:listing_id>", views.delete_listing, name="delete_listing"),
    path("get_subcategories/", views.get_subcategories, name="get_subcategories"),
    path(
        "get_all_subcategories/",
        views.get_all_subcategories,
        name="get_all_subcategories",
    ),
]
