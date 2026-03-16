"""Preview mode middleware - persists ?preview=1 across pages via session."""
from django.shortcuts import redirect


class PreviewModeMiddleware:
    """Set preview_mode in session when ?preview=1, clear when ?exit_preview=1."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Session must exist (SessionMiddleware runs before this)
        if hasattr(request, "session"):
            if request.GET.get("exit_preview"):
                request.session.pop("preview_mode", None)
                from urllib.parse import urlencode
                base = request.path
                qs = {k: v for k, v in request.GET.items() if k != "exit_preview"}
                qs_str = ("?" + urlencode(qs)) if qs else ""
                return redirect(base + qs_str)
            if request.GET.get("preview") == "1" and getattr(request.user, "is_staff", False):
                request.session["preview_mode"] = True

        return self.get_response(request)
