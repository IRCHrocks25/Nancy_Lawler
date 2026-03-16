"""Dashboard URL configuration."""
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.dashboard_login, name="dashboard_login"),
    path("logout/", views.dashboard_logout, name="dashboard_logout"),
    path("", views.dashboard_home, name="dashboard_home"),
    path("content/", views.dashboard_content, name="dashboard_content"),
    path("content/save/", views.dashboard_content_save, name="dashboard_content_save"),
    path("content/preview/", views.dashboard_content_preview, name="dashboard_content_preview"),
    path("preview/publish/", views.dashboard_preview_publish, name="dashboard_preview_publish"),
    path("images/", views.dashboard_images, name="dashboard_images"),
    path("images/save/", views.dashboard_image_save, name="dashboard_image_save"),
    path("images/upload/", views.dashboard_image_upload, name="dashboard_image_upload"),
    path("ctas/", views.dashboard_ctas, name="dashboard_ctas"),
    path("ctas/save/", views.dashboard_cta_save, name="dashboard_cta_save"),
    path("ctas/save/<int:pk>/", views.dashboard_cta_save, name="dashboard_cta_edit"),
    path("ctas/delete/<int:pk>/", views.dashboard_cta_delete, name="dashboard_cta_delete"),
    path("testimonials/", views.dashboard_testimonials, name="dashboard_testimonials"),
    path("testimonials/save/", views.dashboard_testimonial_save, name="dashboard_testimonial_save"),
    path("testimonials/save/<int:pk>/", views.dashboard_testimonial_save, name="dashboard_testimonial_edit"),
    path("testimonials/delete/<int:pk>/", views.dashboard_testimonial_delete, name="dashboard_testimonial_delete"),
    path("social/", views.dashboard_social, name="dashboard_social"),
    path("social/save/", views.dashboard_social_save, name="dashboard_social_save"),
    path("social/delete/<int:pk>/", views.dashboard_social_delete, name="dashboard_social_delete"),
    path("contact/save/", views.dashboard_contact_save, name="dashboard_contact_save"),
    path("history/", views.dashboard_history, name="dashboard_history"),
    path("history/delete/<int:pk>/", views.dashboard_history_delete, name="dashboard_history_delete"),
]
