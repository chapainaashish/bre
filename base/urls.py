from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("page/<slug:slug>/", views.page, name="page"),
    path("error_404/", views.error_404, name="error_404"),
]
