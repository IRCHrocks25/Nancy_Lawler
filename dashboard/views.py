"""Dashboard views: login, content, CTAs, testimonials, social, history."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse
from django.contrib import messages

from .models import ContentItem, PreviewDraft, CTA, Testimonial, SocialLink, ContactInfo, ChangeHistory
from .content_keys import CONTENT_KEYS, CONTENT_GROUPS, IMAGE_KEYS
from .default_content import DEFAULT_CONTENT
from .utils import log_change, get_content_dict


def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard_home")
    ctx = {}
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            next_url = request.GET.get("next") or "dashboard_home"
            return redirect(next_url)
        ctx["error"] = "Invalid credentials or not staff."
    return render(request, "dashboard/login.html", ctx)


def dashboard_logout(request):
    logout(request)
    return redirect("dashboard_login")


@login_required(login_url="/dashboard/login/")
def dashboard_home(request):
    recent = ChangeHistory.objects.all()[:15]
    return render(request, "dashboard/home.html", {"recent_changes": recent})


@login_required(login_url="/dashboard/login/")
def dashboard_content(request):
    content = dict(DEFAULT_CONTENT)
    for c in ContentItem.objects.all():
        content[c.key] = c.value
    return render(request, "dashboard/content.html", {
        "content": content,
        "content_groups": CONTENT_GROUPS,
        "default_content": DEFAULT_CONTENT,
    })


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_content_save(request):
    for key in request.POST:
        if key.startswith("content_"):
            content_key = key.replace("content_", "", 1)
            if content_key in CONTENT_KEYS:
                val = request.POST.get(key, "")
                obj, _ = ContentItem.objects.get_or_create(key=content_key, defaults={"value": val})
                old_val = obj.value
                obj.value = val
                obj.save()
                log_change("ContentItem", obj.pk, "update", {"key": content_key, "old": old_val, "new": val}, request.user)
    messages.success(request, "Saved! Changes are now live.")
    return redirect("dashboard_content")


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_content_preview(request):
    for key in request.POST:
        if key.startswith("content_"):
            content_key = key.replace("content_", "", 1)
            if content_key in CONTENT_KEYS:
                val = request.POST.get(key, "")
                PreviewDraft.objects.update_or_create(key=content_key, defaults={"value": val})
    return redirect("/?preview=1")


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_preview_publish(request):
    if hasattr(request, "session"):
        request.session.pop("preview_mode", None)
    for d in PreviewDraft.objects.all():
        obj, _ = ContentItem.objects.get_or_create(key=d.key, defaults={"value": d.value})
        obj.value = d.value
        obj.save()
        log_change("ContentItem", obj.pk, "publish_preview", {"key": d.key}, request.user)
    PreviewDraft.objects.all().delete()
    messages.success(request, "Preview published. Changes are now live.")
    return redirect("/")


@login_required(login_url="/dashboard/login/")
def dashboard_images(request):
    """Images dashboard: edit URLs and upload to Cloudinary."""
    from django.conf import settings
    import os
    content = dict(DEFAULT_CONTENT)
    for c in ContentItem.objects.all():
        content[c.key] = c.value
    cloudinary_configured = bool(
        getattr(settings, "CLOUDINARY_URL", "")
        or (getattr(settings, "CLOUDINARY_API_KEY", "") and getattr(settings, "CLOUDINARY_API_SECRET", ""))
    )
    return render(request, "dashboard/images.html", {
        "content": content,
        "image_keys": IMAGE_KEYS,
        "cloudinary_configured": cloudinary_configured,
    })


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_image_save(request):
    """Save image URL from form."""
    for key, _ in IMAGE_KEYS:
        field = "image_" + key.replace(".", "_")
        val = request.POST.get(field, "").strip()
        obj, _ = ContentItem.objects.get_or_create(key=key, defaults={"value": val})
        obj.value = val
        obj.save()
        log_change("ContentItem", obj.pk, "update", {"key": key}, request.user)
    messages.success(request, "Saved! Image URLs are now live.")
    return redirect("dashboard_images")


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_image_upload(request):
    """Upload file to Cloudinary and save URL to the specified content key."""
    from django.conf import settings
    import os
    key = request.POST.get("image_key", "").strip()
    if key not in [k for k, _ in IMAGE_KEYS]:
        return redirect("dashboard_images")
    file_obj = request.FILES.get("file")
    if not file_obj:
        return redirect("dashboard_images")
    try:
        import cloudinary.uploader
        import cloudinary
        cloud_url = getattr(settings, "CLOUDINARY_URL", "") or os.environ.get("CLOUDINARY_URL", "")
        if cloud_url:
            cloudinary.config(cloudinary_url=cloud_url)
        else:
            cloudinary.config(
                cloud_name=getattr(settings, "CLOUDINARY_CLOUD_NAME", ""),
                api_key=getattr(settings, "CLOUDINARY_API_KEY", ""),
                api_secret=getattr(settings, "CLOUDINARY_API_SECRET", ""),
            )
        result = cloudinary.uploader.upload(
            file_obj,
            folder="lawlerai",
            resource_type="auto",
        )
        url = result.get("secure_url", result.get("url", ""))
        if url:
            obj, _ = ContentItem.objects.get_or_create(key=key, defaults={"value": url})
            obj.value = url
            obj.save()
            log_change("ContentItem", obj.pk, "upload", {"key": key, "url": url}, request.user)
    except Exception as e:
        messages.error(request, f"Upload failed: {e}")
    return redirect("dashboard_images")


@login_required(login_url="/dashboard/login/")
def dashboard_ctas(request):
    ctas = CTA.objects.all()
    edit_cta = None
    if request.GET.get("edit"):
        try:
            edit_cta = CTA.objects.get(pk=request.GET.get("edit"))
        except CTA.DoesNotExist:
            pass
    return render(request, "dashboard/ctas.html", {"ctas": ctas, "edit_cta": edit_cta})


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_cta_save(request, pk=None):
    cta = get_object_or_404(CTA, pk=pk) if pk else None
    if cta:
        cta.label = request.POST.get("label", "")
        cta.url = request.POST.get("url", "")
        cta.placement = request.POST.get("placement", "hero")
        cta.order = int(request.POST.get("order") or 0)
        cta.is_active = request.POST.get("is_active") == "on"
        cta.save()
        log_change("CTA", cta.pk, "update", {}, request.user)
    else:
        cta = CTA.objects.create(
            label=request.POST.get("label", ""),
            url=request.POST.get("url", ""),
            placement=request.POST.get("placement", "hero"),
            order=int(request.POST.get("order") or 0),
            is_active=request.POST.get("is_active") == "on",
        )
        log_change("CTA", cta.pk, "create", {}, request.user)
    messages.success(request, "Saved! CTA changes are now live.")
    return redirect("dashboard_ctas")


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_cta_delete(request, pk):
    cta = get_object_or_404(CTA, pk=pk)
    cta.delete()
    log_change("CTA", pk, "delete", {}, request.user)
    return redirect("dashboard_ctas")


@login_required(login_url="/dashboard/login/")
def dashboard_testimonials(request):
    testimonials = Testimonial.objects.all()
    edit_testimonial = None
    if request.GET.get("edit"):
        try:
            edit_testimonial = Testimonial.objects.get(pk=request.GET.get("edit"))
        except Testimonial.DoesNotExist:
            pass
    return render(request, "dashboard/testimonials.html", {"testimonials": testimonials, "edit_testimonial": edit_testimonial})


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_testimonial_save(request, pk=None):
    t = get_object_or_404(Testimonial, pk=pk) if pk else None
    if t:
        t.quote = request.POST.get("quote", "")
        t.author_name = request.POST.get("author_name", "")
        t.author_role = request.POST.get("author_role", "")
        t.author_org = request.POST.get("author_org", "")
        t.order = int(request.POST.get("order") or 0)
        t.is_active = request.POST.get("is_active") == "on"
        t.save()
        log_change("Testimonial", t.pk, "update", {}, request.user)
    else:
        t = Testimonial.objects.create(
            quote=request.POST.get("quote", ""),
            author_name=request.POST.get("author_name", ""),
            author_role=request.POST.get("author_role", ""),
            author_org=request.POST.get("author_org", ""),
            order=int(request.POST.get("order") or 0),
            is_active=request.POST.get("is_active") == "on",
        )
        log_change("Testimonial", t.pk, "create", {}, request.user)
    messages.success(request, "Saved! Testimonial changes are now live.")
    return redirect("dashboard_testimonials")


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_testimonial_delete(request, pk):
    t = get_object_or_404(Testimonial, pk=pk)
    t.delete()
    log_change("Testimonial", pk, "delete", {}, request.user)
    return redirect("dashboard_testimonials")


@login_required(login_url="/dashboard/login/")
def dashboard_social(request):
    social = SocialLink.objects.all()
    contact = {c.key: c.value for c in ContactInfo.objects.all()}
    return render(request, "dashboard/social.html", {"social": social, "contact": contact})


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_social_save(request):
    platform = request.POST.get("platform", "").strip()
    url = request.POST.get("url", "").strip()
    if platform and url:
        SocialLink.objects.create(platform=platform, url=url)
        log_change("SocialLink", "", "create", {}, request.user)
        messages.success(request, "Saved! Social link is now live.")
    return redirect("dashboard_social")


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_social_delete(request, pk):
    sl = get_object_or_404(SocialLink, pk=pk)
    sl.delete()
    log_change("SocialLink", pk, "delete", {}, request.user)
    return redirect("dashboard_social")


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_contact_save(request):
    for k, v in request.POST.items():
        if k.startswith("contact_") and k != "csrfmiddlewaretoken":
            key = k.replace("contact_", "", 1)
            obj, _ = ContactInfo.objects.get_or_create(key=key, defaults={"value": v})
            obj.value = v
            obj.save()
    messages.success(request, "Saved! Contact details are now live.")
    return redirect("dashboard_social")


@login_required(login_url="/dashboard/login/")
def dashboard_history(request):
    history = ChangeHistory.objects.all()[:50]
    return render(request, "dashboard/history.html", {"history": history})


@login_required(login_url="/dashboard/login/")
@require_POST
def dashboard_history_delete(request, pk):
    h = get_object_or_404(ChangeHistory, pk=pk)
    h.delete()
    return redirect("dashboard_history")
