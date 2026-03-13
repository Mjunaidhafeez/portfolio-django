import textwrap
import zipfile
from io import BytesIO
from pathlib import Path
from urllib.parse import quote_plus

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import (
    BlogBlock,
    BlogCategory,
    BlogComment,
    BlogPost,
    BlogTag,
    ContactMessage,
    DownloadCategory,
    DownloadItem,
    PortfolioSection,
    SectionEntry,
    SiteSettings,
)


def _visible_sections(show_on_resume=False):
    sections = PortfolioSection.objects.filter(is_visible=True)
    if show_on_resume:
        sections = sections.filter(show_on_resume=True)
    return sections.prefetch_related(
        Prefetch(
            "entries",
            queryset=SectionEntry.objects.filter(is_visible=True).order_by("order", "id"),
        )
    )


def home(request):
    context = {
        "sections": _visible_sections(show_on_resume=False),
        "site_settings": SiteSettings.get_solo(),
    }
    return render(request, "home.html", context)


def resume(request):
    context = {
        "resume_sections": _visible_sections(show_on_resume=True),
        "site_settings": SiteSettings.get_solo(),
        "is_preview": False,
        "preview_action": "",
    }
    return render(request, "resume.html", context)


def resume_preview(request):
    context = {
        "resume_sections": _visible_sections(show_on_resume=True),
        "site_settings": SiteSettings.get_solo(),
        "is_preview": True,
        "preview_action": request.GET.get("action", ""),
    }
    return render(request, "resume_preview.html", context)


def blog_list(request):
    search_query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    tag_slug = request.GET.get("tag", "").strip()

    posts = (
        BlogPost.objects.filter(is_published=True)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-published_at", "-id")
    )
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query)
            | Q(excerpt__icontains=search_query)
            | Q(content__icontains=search_query)
        )
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    context = {
        "posts": posts.distinct(),
        "search_query": search_query,
        "active_category": category_slug,
        "active_tag": tag_slug,
        "categories": BlogCategory.objects.filter(is_active=True),
        "tags": BlogTag.objects.filter(is_active=True),
        "site_settings": SiteSettings.get_solo(),
    }
    return render(request, "blog_list.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.prefetch_related(
            Prefetch(
                "blocks",
                queryset=BlogBlock.objects.filter(is_visible=True).order_by("order", "id"),
            )
        ),
        slug=slug,
        is_published=True,
    )
    context = {
        "post": post,
        "comments": post.comments.filter(is_approved=True),
        "comment_submitted": request.GET.get("comment") == "submitted",
        "site_settings": SiteSettings.get_solo(),
    }
    return render(request, "blog_detail.html", context)


@require_POST
def blog_comment_create(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    message = request.POST.get("message", "").strip()

    if name and email and message:
        BlogComment.objects.create(
            post=post,
            name=name,
            email=email,
            message=message,
            is_approved=False,
        )
        return redirect(f"/blogs/{post.slug}/?comment=submitted#comments")

    return redirect(f"/blogs/{post.slug}/#comments")


def download_list(request):
    category_slug = request.GET.get("category", "").strip()
    selected_category = None
    categories = DownloadCategory.objects.filter(is_active=True).select_related("parent")
    items = DownloadItem.objects.filter(is_published=True).select_related("category")

    if category_slug:
        selected_category = get_object_or_404(categories, slug=category_slug)
        items = items.filter(category=selected_category)
        child_categories = categories.filter(parent=selected_category).order_by("order", "name")
    else:
        items = items.filter(category__isnull=True)
        child_categories = categories.filter(parent__isnull=True).order_by("order", "name")

    items = items.order_by("order", "-uploaded_at", "-id")

    breadcrumbs = []
    if selected_category:
        breadcrumbs = selected_category.get_ancestors() + [selected_category]

    context = {
        "items": items,
        "child_categories": child_categories,
        "selected_category": selected_category,
        "breadcrumbs": breadcrumbs,
        "site_settings": SiteSettings.get_solo(),
    }
    return render(request, "download_list.html", context)


def download_detail(request, slug):
    item = get_object_or_404(DownloadItem, slug=slug, is_published=True)
    preview_text = ""
    preview_rows = []

    if item.preview_type in {"text", "csv"}:
        try:
            file_path = Path(item.file.path)
            if file_path.exists():
                with file_path.open("r", encoding="utf-8", errors="replace") as f:
                    lines = f.readlines()[:40]
                if item.preview_type == "csv":
                    preview_rows = [line.rstrip("\n").split(",") for line in lines]
                else:
                    preview_text = "".join(lines)
        except Exception:
            preview_text = ""
            preview_rows = []

    office_preview_url = ""

    if item.preview_type == "office":
        file_abs_url = request.build_absolute_uri(item.file.url)
        office_preview_url = f"https://view.officeapps.live.com/op/embed.aspx?src={quote_plus(file_abs_url)}"

    context = {
        "item": item,
        "preview_text": preview_text,
        "preview_rows": preview_rows,
        "office_preview_url": office_preview_url,
        "site_settings": SiteSettings.get_solo(),
    }
    return render(request, "download_detail.html", context)


@require_POST
def download_bulk(request):
    item_ids = request.POST.getlist("item_ids")
    if not item_ids:
        return redirect("/downloads/")

    items = DownloadItem.objects.filter(is_published=True, id__in=item_ids)
    if not items.exists():
        return redirect("/downloads/")

    zip_buffer = BytesIO()
    used_names = {}
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for item in items:
            try:
                file_path = Path(item.file.path)
                if not file_path.exists():
                    continue
                arcname = item.file_name
                if arcname in used_names:
                    used_names[arcname] += 1
                    stem = file_path.stem
                    suffix = file_path.suffix
                    arcname = f"{stem}_{used_names[arcname]}{suffix}"
                else:
                    used_names[arcname] = 1
                zip_file.write(file_path, arcname=arcname)
            except Exception:
                continue

    zip_buffer.seek(0)
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="downloads_{timestamp}.zip"'
    return response


@require_POST
def contact_view(request):
    try:
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        site_settings = SiteSettings.get_solo()
        if not all([name, email, subject, message]):
            return JsonResponse(
                {"status": "error", "message": site_settings.contact_required_fields_error},
                status=400,
            )

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        recipient = site_settings.email or settings.EMAIL_HOST_USER
        email_message = (
            f"{site_settings.contact_name_label}: {name}\n"
            f"{site_settings.contact_email_label}: {email}\n"
            f"{site_settings.contact_subject_label}: {subject}\n\n"
            f"{site_settings.contact_message_label}:\n{message}"
        )

        mail_error = False
        try:
            send_mail(
                subject=f"{site_settings.contact_email_subject_prefix}: {subject}",
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception:
            mail_error = True

        if mail_error:
            return JsonResponse(
                {
                    "status": "success",
                    "message": site_settings.contact_saved_only_message,
                }
            )

        return JsonResponse({"status": "success", "message": site_settings.contact_success_message})
    except Exception:
        site_settings = SiteSettings.get_solo()
        return JsonResponse(
            {
                "status": "error",
                "message": site_settings.contact_failure_message,
            },
            status=500,
        )


def _draw_line(doc, text, x, y, font="Helvetica", size=10, color=colors.black):
    doc.setFillColor(color)
    doc.setFont(font, size)
    doc.drawString(x, y, text)


def _draw_header(doc, width, height, site_settings):
    doc.setFillColor(colors.HexColor("#0f172a"))
    doc.rect(0, height - 110, width, 110, fill=1, stroke=0)
    _draw_line(
        doc,
        site_settings.full_name.upper(),
        42,
        height - 54,
        font="Helvetica-Bold",
        size=22,
        color=colors.white,
    )
    _draw_line(
        doc,
        site_settings.professional_title,
        42,
        height - 76,
        font="Helvetica",
        size=11,
        color=colors.HexColor("#bae6fd"),
    )
    contact_items = [site_settings.email, site_settings.phone, site_settings.address]
    contact_line = "  |  ".join([item for item in contact_items if item])
    if contact_line:
        _draw_line(
            doc,
            contact_line,
            42,
            height - 95,
            font="Helvetica",
            size=8,
            color=colors.HexColor("#cbd5e1"),
        )


def _new_page_if_needed(doc, y, site_settings, width, height, min_y=64):
    if y >= min_y:
        return y
    doc.showPage()
    _draw_header(doc, width, height, site_settings)
    return height - 132


def generate_pdf(request):
    site_settings = SiteSettings.get_solo()
    sections = _visible_sections(show_on_resume=True)

    response = HttpResponse(content_type="application/pdf")
    filename = f"{site_settings.resume_filename.strip() or 'resume'}.pdf"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    doc = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    _draw_header(doc, width, height, site_settings)
    y = height - 132

    if site_settings.about_text:
        _draw_line(
            doc,
            site_settings.pdf_profile_summary_title,
            42,
            y,
            font="Helvetica-Bold",
            size=11,
            color=colors.HexColor("#0f172a"),
        )
        y -= 16
        for line in textwrap.wrap(site_settings.about_text, width=96):
            y = _new_page_if_needed(doc, y, site_settings, width, height)
            _draw_line(doc, line, 42, y, size=10, color=colors.HexColor("#0f172a"))
            y -= 14
        y -= 8

    for section in sections:
        y = _new_page_if_needed(doc, y, site_settings, width, height)
        doc.setFillColor(colors.HexColor("#e2e8f0"))
        doc.roundRect(38, y - 11, width - 76, 18, 4, stroke=0, fill=1)
        _draw_line(
            doc,
            section.title.upper(),
            44,
            y - 5,
            font="Helvetica-Bold",
            size=10,
            color=colors.HexColor("#0f172a"),
        )
        y -= 16

        if section.description:
            for line in textwrap.wrap(section.description, width=96):
                y = _new_page_if_needed(doc, y, site_settings, width, height)
                _draw_line(doc, line, 42, y, size=9, color=colors.HexColor("#334155"))
                y -= 14
            y -= 6

        for entry in section.entries.all():
            y = _new_page_if_needed(doc, y, site_settings, width, height)
            _draw_line(doc, entry.title, 42, y, font="Helvetica-Bold", size=10, color=colors.HexColor("#0f172a"))
            y -= 14

            meta = " | ".join([part for part in [entry.subtitle, entry.date_range, entry.location] if part])
            if meta:
                _draw_line(doc, meta, 42, y, size=8, color=colors.HexColor("#475569"))
                y -= 13

            if entry.description:
                for line in textwrap.wrap(entry.description, width=92):
                    y = _new_page_if_needed(doc, y, site_settings, width, height)
                    _draw_line(doc, line, 54, y, size=9, color=colors.HexColor("#1e293b"))
                    y -= 12

            for bullet in entry.bullets_list:
                for line in textwrap.wrap(f"- {bullet}", width=90):
                    y = _new_page_if_needed(doc, y, site_settings, width, height)
                    _draw_line(doc, line, 54, y, size=9, color=colors.HexColor("#1e293b"))
                    y -= 12

            if entry.tags_list:
                tags_line = ", ".join(entry.tags_list)
                for line in textwrap.wrap(f"{site_settings.pdf_technologies_label}: {tags_line}", width=90):
                    y = _new_page_if_needed(doc, y, site_settings, width, height)
                    _draw_line(doc, line, 54, y, size=8, color=colors.HexColor("#0369a1"))
                    y -= 12
            y -= 6

    doc.save()
    return response
