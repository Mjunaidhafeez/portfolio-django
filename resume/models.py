import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

_HEX_COLOR_RE = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")


def validate_optional_hex_color(value: str) -> None:
    if not value:
        return
    if not _HEX_COLOR_RE.match(value.strip()):
        raise ValidationError("Enter a valid hex color such as #e8eef7 or #abc.")


def strip_optional_hex_fields(obj, field_names: tuple[str, ...]) -> None:
    for name in field_names:
        val = getattr(obj, name, None)
        if isinstance(val, str):
            setattr(obj, name, val.strip())


_SITE_SETTINGS_HEX_COLOR_FIELDS = (
    "home_name_color",
    "home_title_color",
    "home_welcome_title_color",
    "home_hero_intro_color",
    "about_title_color",
    "about_subtitle_color",
    "about_body_color",
    "contact_section_title_color",
    "contact_section_subtitle_color",
    "contact_body_color",
)

_PORTFOLIO_SECTION_HEX_COLOR_FIELDS = (
    "title_color",
    "description_color",
    "body_text_color",
)


class SiteSettings(models.Model):
    THEME_OCEAN = "ocean"
    THEME_EMERALD = "emerald"
    THEME_SUNSET = "sunset"
    THEME_MONO = "mono"
    THEME_ROYAL = "royal"
    THEME_CRIMSON = "crimson"
    THEME_AURORA = "aurora"
    COLOR_THEME_CHOICES = (
        (THEME_OCEAN, "Ocean Blue"),
        (THEME_EMERALD, "Emerald Pro"),
        (THEME_SUNSET, "Sunset Glow"),
        (THEME_MONO, "Monochrome Luxe"),
        (THEME_ROYAL, "Royal Purple"),
        (THEME_CRIMSON, "Crimson Night"),
        (THEME_AURORA, "Aurora Mint"),
    )

    full_name = models.CharField(max_length=120, default="Your Name")
    professional_title = models.CharField(max_length=180, default="Software Engineer")
    hero_intro = models.TextField(blank=True)
    about_text = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    profile_image = models.CharField(
        max_length=255,
        blank=True,
        default="images/junaid.jpg",
        help_text="Path relative to static folder, e.g. images/profile.jpg",
    )
    profile_photo = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
        help_text="Upload profile image from admin panel.",
    )
    site_background_image = models.ImageField(
        upload_to="backgrounds/site/",
        blank=True,
        null=True,
        help_text="Optional full-website background image with subtle reflection overlay.",
    )
    color_theme = models.CharField(
        max_length=20,
        choices=COLOR_THEME_CHOICES,
        default=THEME_OCEAN,
        help_text="Select a complete color theme for the website.",
    )
    home_name_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Hero: your name (hex, e.g. #e8eef7). Blank = theme default.",
    )
    home_title_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Hero: professional title line.",
    )
    home_welcome_title_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Hero: welcome heading.",
    )
    home_hero_intro_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Hero: intro paragraph under welcome.",
    )
    about_title_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="About section: main heading.",
    )
    about_subtitle_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="About section: subtitle.",
    )
    about_body_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="About section: body paragraph.",
    )
    contact_section_title_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Contact: main section title.",
    )
    contact_section_subtitle_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Contact: subtitle under title.",
    )
    contact_body_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Contact: card text, labels, and form labels.",
    )
    footer_text = models.CharField(max_length=255, blank=True, default="All rights reserved.")
    resume_filename = models.CharField(max_length=120, default="resume")
    footer_contact_title = models.CharField(max_length=120, default="Contact Information")
    footer_links_title = models.CharField(max_length=120, default="Quick Links")
    footer_social_title = models.CharField(max_length=120, default="Connect With Me")
    home_welcome_title = models.CharField(max_length=180, default="Welcome to my professional portfolio")
    home_about_title = models.CharField(max_length=120, default="About Me")
    home_open_link_text = models.CharField(max_length=80, default="Open Link")
    home_no_entries_text = models.CharField(
        max_length=180,
        default="No entries added yet. Add content from admin panel.",
    )
    contact_section_title = models.CharField(max_length=120, default="Get in Touch")
    contact_section_subtitle = models.CharField(
        max_length=180,
        default="Feel free to reach out through the details below or the message form.",
    )
    contact_info_title = models.CharField(max_length=120, default="Contact Information")
    contact_form_title = models.CharField(max_length=120, default="Send a Message")
    contact_name_label = models.CharField(max_length=60, default="Name")
    contact_email_label = models.CharField(max_length=60, default="Email")
    contact_phone_label = models.CharField(max_length=60, default="Phone")
    contact_address_label = models.CharField(max_length=60, default="Address")
    contact_linkedin_label = models.CharField(max_length=60, default="LinkedIn")
    contact_website_label = models.CharField(max_length=60, default="Website")
    contact_subject_label = models.CharField(max_length=60, default="Subject")
    contact_message_label = models.CharField(max_length=60, default="Message")
    contact_send_button_text = models.CharField(max_length=80, default="Send Message")
    contact_required_fields_error = models.CharField(max_length=180, default="All fields are required.")
    contact_success_message = models.CharField(
        max_length=180,
        default="Your message has been sent successfully!",
    )
    contact_saved_only_message = models.CharField(
        max_length=180,
        default="Message saved successfully. Email delivery is currently unavailable.",
    )
    contact_failure_message = models.CharField(
        max_length=180,
        default="There was an error sending your message. Please try again later.",
    )
    contact_email_subject_prefix = models.CharField(max_length=120, default="Portfolio Contact Form")
    resume_page_title = models.CharField(max_length=120, default="Professional Resume")
    resume_page_subtitle = models.CharField(
        max_length=180,
        default="A comprehensive overview of my professional journey, skills, and achievements.",
    )
    resume_profile_title = models.CharField(max_length=120, default="Professional Summary")
    resume_download_button_text = models.CharField(max_length=120, default="Download Resume")
    resume_print_button_text = models.CharField(max_length=120, default="Print Resume")
    resume_no_sections_text = models.CharField(
        max_length=180,
        default="No resume sections are configured yet. Add sections from admin panel.",
    )
    pdf_profile_summary_title = models.CharField(max_length=80, default="PROFILE SUMMARY")
    pdf_technologies_label = models.CharField(max_length=80, default="Technologies")
    blog_page_title = models.CharField(max_length=120, default="Latest Blogs")
    blog_page_subtitle = models.CharField(
        max_length=180,
        default="Thoughts, updates, and practical notes from daily work.",
    )
    blog_search_placeholder = models.CharField(max_length=120, default="Search blogs...")
    blog_search_button_text = models.CharField(max_length=40, default="Search")
    blog_filter_all_text = models.CharField(max_length=40, default="All")
    blog_categories_title = models.CharField(max_length=80, default="Categories")
    blog_tags_title = models.CharField(max_length=80, default="Tags")
    blog_category_label_text = models.CharField(max_length=80, default="Category")
    blog_read_more_text = models.CharField(max_length=80, default="Read More")
    blog_no_posts_text = models.CharField(max_length=180, default="No blogs published yet.")
    blog_back_to_blogs_text = models.CharField(max_length=80, default="Back to Blogs")
    blog_comments_title = models.CharField(max_length=80, default="Comments")
    blog_comment_name_label = models.CharField(max_length=60, default="Name")
    blog_comment_email_label = models.CharField(max_length=60, default="Email")
    blog_comment_message_label = models.CharField(max_length=60, default="Message")
    blog_comment_submit_text = models.CharField(max_length=80, default="Post Comment")
    blog_comment_pending_text = models.CharField(
        max_length=180,
        default="Your comment was submitted and will appear after approval.",
    )
    blog_no_comments_text = models.CharField(max_length=120, default="No comments yet.")
    downloads_page_title = models.CharField(max_length=120, default="Downloads")
    downloads_page_subtitle = models.CharField(
        max_length=180,
        default="Access useful files, resources, and documents.",
    )
    downloads_open_text = models.CharField(max_length=80, default="Open")
    downloads_download_text = models.CharField(max_length=80, default="Download")
    downloads_bulk_download_text = models.CharField(max_length=120, default="Download Selected (ZIP)")
    downloads_categories_title = models.CharField(max_length=120, default="Categories")
    downloads_filter_all_text = models.CharField(max_length=40, default="All")
    downloads_select_item_text = models.CharField(max_length=80, default="Select")
    downloads_no_items_text = models.CharField(max_length=180, default="No files uploaded yet.")
    downloads_back_text = models.CharField(max_length=80, default="Back to Downloads")
    downloads_preview_unavailable_text = models.CharField(
        max_length=180,
        default="Preview is not available for this file type. Use download button.",
    )
    downloads_office_preview_note = models.CharField(
        max_length=180,
        default="Office preview may require internet/public URL access.",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        strip_optional_hex_fields(self, _SITE_SETTINGS_HEX_COLOR_FIELDS)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        settings = cls.objects.first()
        if settings:
            return settings
        return cls.objects.create(pk=1)

    def __str__(self):
        return "Portfolio Settings"


class PortfolioSection(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    nav_title = models.CharField(max_length=80, blank=True)
    headline = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=80, blank=True, default="fas fa-star")
    background_image = models.ImageField(
        upload_to="backgrounds/sections/",
        blank=True,
        null=True,
        help_text="Optional background image for this section only.",
    )
    title_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Section headline (hex). Blank = theme default.",
    )
    description_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Section description line.",
    )
    body_text_color = models.CharField(
        max_length=7,
        blank=True,
        validators=[validate_optional_hex_color],
        help_text="Project cards: titles, body, bullets (not tag pills).",
    )
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    show_on_resume = models.BooleanField(
        default=True,
        verbose_name="Show on CV/Resume",
        help_text="Enable to include this section on Resume preview and PDF.",
    )

    class Meta:
        ordering = ["order", "id"]

    def save(self, *args, **kwargs):
        strip_optional_hex_fields(self, _PORTFOLIO_SECTION_HEX_COLOR_FIELDS)
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SectionEntry(models.Model):
    section = models.ForeignKey(PortfolioSection, on_delete=models.CASCADE, related_name="entries")
    title = models.CharField(max_length=180)
    subtitle = models.CharField(max_length=180, blank=True)
    date_range = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    bullet_points = models.TextField(
        blank=True,
        help_text="Write one bullet per line for best formatting.",
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma separated tags, e.g. Django, Python, AWS",
    )
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def bullets_list(self):
        if not self.bullet_points:
            return []
        lines = [line.strip() for line in self.bullet_points.splitlines() if line.strip()]
        return lines

    @property
    def tags_list(self):
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]


class NavigationItem(models.Model):
    label = models.CharField(max_length=80)
    section = models.ForeignKey(
        PortfolioSection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="navigation_items",
        help_text="If selected, URL will automatically use #section-slug",
    )
    custom_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Use for internal or external links when section is not selected.",
    )
    open_in_new_tab = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label

    @property
    def resolved_url(self):
        if self.section:
            return f"/#{self.section.slug}"
        return self.custom_url or "/"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class BlogPost(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True, help_text="Main introductory body text.")
    category = models.ForeignKey(
        "BlogCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField("BlogTag", blank=True, related_name="posts")
    cover_image = models.ImageField(upload_to="blogs/covers/", blank=True, null=True)
    author_name = models.CharField(max_length=120, default="Admin")
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "blog-post"
            slug = base_slug
            index = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                index += 1
                slug = f"{base_slug}-{index}"
            self.slug = slug
        super().save(*args, **kwargs)


class BlogCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogTag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogBlock(models.Model):
    TYPE_TEXT = "text"
    TYPE_IMAGE = "image"
    TYPE_VIDEO = "video"
    BLOCK_TYPES = (
        (TYPE_TEXT, "Text"),
        (TYPE_IMAGE, "Image"),
        (TYPE_VIDEO, "Video"),
    )

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="blocks")
    block_type = models.CharField(max_length=12, choices=BLOCK_TYPES, default=TYPE_TEXT)
    heading = models.CharField(max_length=180, blank=True)
    text_content = models.TextField(blank=True)
    image = models.ImageField(upload_to="blogs/blocks/images/", blank=True, null=True)
    video_file = models.FileField(upload_to="blogs/blocks/videos/", blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="External video URL (YouTube/Vimeo/MP4).")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.post.title} - {self.block_type} - {self.order}"


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} on {self.post.title}"


class DownloadItem(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        "DownloadCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )
    file = models.FileField(upload_to="downloads/files/")
    thumbnail = models.ImageField(upload_to="downloads/thumbnails/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-uploaded_at", "-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "download-item"
            slug = base_slug
            index = 1
            while DownloadItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                index += 1
                slug = f"{base_slug}-{index}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def file_name(self):
        return self.file.name.split("/")[-1]

    @property
    def file_extension(self):
        if "." not in self.file_name:
            return ""
        return self.file_name.rsplit(".", 1)[-1].lower()

    @property
    def preview_type(self):
        ext = self.file_extension
        if ext in {"pdf"}:
            return "pdf"
        if ext in {"png", "jpg", "jpeg", "gif", "webp", "svg"}:
            return "image"
        if ext in {"mp4", "webm", "ogg", "mov"}:
            return "video"
        if ext in {"txt", "md", "log"}:
            return "text"
        if ext in {"csv"}:
            return "csv"
        if ext in {"ppt", "pptx", "doc", "docx", "xls", "xlsx"}:
            return "office"
        return "other"


class DownloadCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "download-category"
            slug = base_slug
            index = 1
            while DownloadCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                index += 1
                slug = f"{base_slug}-{index}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_ancestors(self):
        ancestors = []
        node = self.parent
        while node:
            ancestors.insert(0, node)
            node = node.parent
        return ancestors
