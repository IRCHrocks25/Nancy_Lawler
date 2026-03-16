"""Dashboard utilities: get content, log changes, seed defaults."""
from .models import ContentItem, PreviewDraft
from .default_content import DEFAULT_CONTENT


def get_content(key, request=None, default=""):
    """Get content value for key. Uses PreviewDraft when preview_mode (staff only) else ContentItem."""
    val = default or DEFAULT_CONTENT.get(key, "")
    preview_ok = (
        request
        and getattr(request.session, "get", lambda k: False)("preview_mode", False)
        and getattr(request.user, "is_staff", False)
    )
    if preview_ok:
        try:
            draft = PreviewDraft.objects.filter(key=key).order_by("-created_at").first()
            if draft:
                return draft.value or val
        except Exception:
            pass
    try:
        obj = ContentItem.objects.filter(key=key).first()
        if obj:
            return obj.value or val
    except Exception:
        pass
    return val


def get_content_dict(request=None):
    """Return dict of all content keys -> values for template context."""
    result = dict(DEFAULT_CONTENT)
    for c in ContentItem.objects.all():
        result[c.key] = c.value or result.get(c.key, "")
    # Preview drafts override live content when in preview mode (staff only)
    preview_ok = (
        request
        and getattr(request.session, "get", lambda k: False)("preview_mode", False)
        and getattr(request.user, "is_staff", False)
    )
    if preview_ok:
        for d in PreviewDraft.objects.all().order_by("key", "-created_at"):
            result[d.key] = d.value or result.get(d.key, "")
    return result


def log_change(model_name, object_id, action, changes, user=None):
    """Log a change to ChangeHistory."""
    from .models import ChangeHistory
    ChangeHistory.objects.create(
        model_name=model_name,
        object_id=str(object_id),
        action=action,
        changes=changes or {},
        user=user,
    )


def seed_content_if_empty():
    """Seed ContentItem from defaults if empty."""
    if ContentItem.objects.exists():
        return
    for key, value in DEFAULT_CONTENT.items():
        ContentItem.objects.create(key=key, value=value)


def seed_ctas_if_empty():
    """Seed default CTAs if empty."""
    from .models import CTA
    if CTA.objects.exists():
        return
    CTA.objects.create(
        label="Explore Your AI Exposure",
        url="/orientation/",
        placement="hero",
        order=0,
        is_active=True,
    )


def seed_testimonials_if_empty():
    """Seed default testimonials if empty."""
    from .models import Testimonial
    if Testimonial.objects.exists():
        return
    pass  # No defaults needed
