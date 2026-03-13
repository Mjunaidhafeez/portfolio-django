from django.contrib import admin

from .models import (
    BlogBlock,
    BlogCategory,
    BlogComment,
    BlogPost,
    BlogTag,
    ContactMessage,
    DownloadCategory,
    DownloadItem,
    NavigationItem,
    PortfolioSection,
    SectionEntry,
    SiteSettings,
)


class SectionEntryInline(admin.StackedInline):
    model = SectionEntry
    extra = 0
    fields = (
        "title",
        "subtitle",
        "date_range",
        "location",
        "description",
        "bullet_points",
        "tags",
        "link",
        "order",
        "is_visible",
    )
    ordering = ("order", "id")


@admin.register(PortfolioSection)
class PortfolioSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "nav_title", "order", "is_visible", "show_on_resume")
    list_editable = ("order", "is_visible", "show_on_resume")
    list_filter = ("is_visible", "show_on_resume")
    search_fields = ("title", "slug", "headline")
    prepopulated_fields = {"slug": ("title",)}
    actions = ("enable_resume_sections", "disable_resume_sections")
    fieldsets = (
        ("Section Identity", {"fields": ("title", "slug", "nav_title", "headline", "icon_class", "background_image")}),
        ("Display Settings", {"fields": ("description", "order", "is_visible", "show_on_resume")}),
    )
    inlines = [SectionEntryInline]

    @admin.action(description="Show selected sections on CV/Resume")
    def enable_resume_sections(self, request, queryset):
        queryset.update(show_on_resume=True)

    @admin.action(description="Hide selected sections from CV/Resume")
    def disable_resume_sections(self, request, queryset):
        queryset.update(show_on_resume=False)


@admin.register(SectionEntry)
class SectionEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "subtitle", "date_range", "order", "is_visible")
    list_filter = ("section", "is_visible")
    list_editable = ("order", "is_visible")
    search_fields = ("title", "subtitle", "description", "tags")
    fieldsets = (
        ("Entry Identity", {"fields": ("section", "title", "subtitle", "date_range", "location")}),
        ("Content", {"fields": ("description", "bullet_points", "tags", "link")}),
        ("Visibility", {"fields": ("order", "is_visible")}),
    )


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ("label", "section", "custom_url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("label", "custom_url")


class BlogBlockInline(admin.StackedInline):
    model = BlogBlock
    extra = 0
    fields = (
        "block_type",
        "heading",
        "text_content",
        "image",
        "video_file",
        "video_url",
        "caption",
        "order",
        "is_visible",
    )
    ordering = ("order", "id")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author_name", "is_published", "published_at", "updated_at")
    list_filter = ("is_published", "published_at", "category", "tags")
    list_editable = ("is_published",)
    search_fields = ("title", "excerpt", "content", "author_name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    fieldsets = (
        ("Post Content", {"fields": ("title", "slug", "excerpt", "content", "cover_image", "category", "tags")}),
        ("Publishing", {"fields": ("author_name", "is_published", "published_at")}),
    )
    inlines = [BlogBlockInline]


@admin.register(BlogBlock)
class BlogBlockAdmin(admin.ModelAdmin):
    list_display = ("post", "block_type", "heading", "order", "is_visible")
    list_filter = ("block_type", "is_visible")
    list_editable = ("order", "is_visible")
    search_fields = ("post__title", "heading", "text_content", "caption")


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_editable = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    list_editable = ("is_approved",)
    search_fields = ("name", "email", "message", "post__title")
    readonly_fields = ("post", "name", "email", "message", "created_at")
    actions = ("approve_comments", "unapprove_comments")

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Unapprove selected comments")
    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)


@admin.register(DownloadItem)
class DownloadItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "file_name", "is_published", "order", "uploaded_at")
    list_filter = ("is_published", "uploaded_at", "category")
    list_editable = ("is_published", "order")
    search_fields = ("title", "description", "file")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Download File", {"fields": ("title", "slug", "description", "category", "file", "thumbnail")}),
        ("Visibility", {"fields": ("is_published", "order")}),
    )


@admin.register(DownloadCategory)
class DownloadCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "parent")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Primary Identity",
            {
                "fields": (
                    "full_name",
                    "professional_title",
                    "hero_intro",
                    "about_text",
                    "profile_photo",
                    "profile_image",
                    "site_background_image",
                    "color_theme",
                    "footer_text",
                    "resume_filename",
                )
            },
        ),
        (
            "Footer Labels",
            {
                "fields": (
                    "footer_contact_title",
                    "footer_links_title",
                    "footer_social_title",
                )
            },
        ),
        (
            "Home Page Labels",
            {
                "fields": (
                    "home_welcome_title",
                    "home_about_title",
                    "home_open_link_text",
                    "home_no_entries_text",
                )
            },
        ),
        (
            "Contact Labels & Messages",
            {
                "fields": (
                    "contact_section_title",
                    "contact_section_subtitle",
                    "contact_info_title",
                    "contact_form_title",
                    "contact_name_label",
                    "contact_email_label",
                    "contact_phone_label",
                    "contact_address_label",
                    "contact_linkedin_label",
                    "contact_website_label",
                    "contact_subject_label",
                    "contact_message_label",
                    "contact_send_button_text",
                    "contact_required_fields_error",
                    "contact_success_message",
                    "contact_saved_only_message",
                    "contact_failure_message",
                    "contact_email_subject_prefix",
                )
            },
        ),
        (
            "Resume & PDF Labels",
            {
                "fields": (
                    "resume_page_title",
                    "resume_page_subtitle",
                    "resume_profile_title",
                    "resume_download_button_text",
                    "resume_print_button_text",
                    "resume_no_sections_text",
                    "pdf_profile_summary_title",
                    "pdf_technologies_label",
                )
            },
        ),
        (
            "Blog Labels",
            {
                "fields": (
                    "blog_page_title",
                    "blog_page_subtitle",
                    "blog_search_placeholder",
                    "blog_search_button_text",
                    "blog_filter_all_text",
                    "blog_categories_title",
                    "blog_tags_title",
                    "blog_category_label_text",
                    "blog_read_more_text",
                    "blog_no_posts_text",
                    "blog_back_to_blogs_text",
                    "blog_comments_title",
                    "blog_comment_name_label",
                    "blog_comment_email_label",
                    "blog_comment_message_label",
                    "blog_comment_submit_text",
                    "blog_comment_pending_text",
                    "blog_no_comments_text",
                )
            },
        ),
        (
            "Downloads Labels",
            {
                "fields": (
                    "downloads_page_title",
                    "downloads_page_subtitle",
                    "downloads_open_text",
                    "downloads_download_text",
                    "downloads_bulk_download_text",
                    "downloads_categories_title",
                    "downloads_filter_all_text",
                    "downloads_select_item_text",
                    "downloads_no_items_text",
                    "downloads_back_text",
                    "downloads_preview_unavailable_text",
                    "downloads_office_preview_note",
                )
            },
        ),
        (
            "Contact & Profiles",
            {
                "fields": (
                    "email",
                    "phone",
                    "address",
                    "linkedin_url",
                    "github_url",
                    "website_url",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("is_read",)
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    actions = ("mark_as_read", "mark_as_unread")

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
