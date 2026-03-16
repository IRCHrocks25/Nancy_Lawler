"""Dashboard template tags and filters."""
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_content(context, key, default=""):
    """Get content for key. Uses site_content from context or fetches."""
    site_content = context.get("site_content") or {}
    val = site_content.get(key)
    return val if val else default


@register.filter
def get_item(d, key):
    """Get dict item by key."""
    return d.get(key, "") if d else ""


@register.filter
def image_field_name(key):
    """Convert content key to form field name, e.g. nav.logo_url -> image_nav_logo_url."""
    return "image_" + key.replace(".", "_") if key else ""
