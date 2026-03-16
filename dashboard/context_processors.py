"""Context processor to inject site content and preview_mode into templates."""

def dashboard_content(request):
    """Add site_content and preview_mode to template context."""
    from .utils import get_content_dict
    return {
        "site_content": get_content_dict(request),
        "preview_mode": request.session.get("preview_mode", False) if hasattr(request, "session") else False,
    }
