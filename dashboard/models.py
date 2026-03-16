"""Dashboard models for content management, CTAs, testimonials, history."""
from django.db import models
from django.conf import settings


class ContentItem(models.Model):
    key = models.CharField(max_length=200, unique=True, db_index=True)
    value = models.TextField(blank=True)
    value_type = models.CharField(max_length=20, default="text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]


class PreviewDraft(models.Model):
    key = models.CharField(max_length=200, db_index=True)
    value = models.TextField(blank=True)
    value_type = models.CharField(max_length=20, default="text")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["key"]


class CTA(models.Model):
    label = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    placement = models.CharField(max_length=100, default="hero")
    page = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    icon_before = models.CharField(max_length=100, blank=True)
    icon_after = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["placement", "order", "id"]


class Testimonial(models.Model):
    quote = models.TextField()
    author_name = models.CharField(max_length=200)
    author_role = models.CharField(max_length=200, blank=True)
    author_org = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]


class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    label = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]


class ContactInfo(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)


class ChangeHistory(models.Model):
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    action = models.CharField(max_length=50)
    changes = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
