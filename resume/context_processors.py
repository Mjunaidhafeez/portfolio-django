from .models import NavigationItem, SiteSettings


def portfolio_context(request):
    return {
        "site_settings": SiteSettings.get_solo(),
        "navigation_items": NavigationItem.objects.filter(is_active=True).select_related("section"),
    }
