from wagtail.models import Page, Locale

def navbar(request):
    locale = Locale.objects.get(language_code=request.LANGUAGE_CODE)
    return {
        "navbar_pages": Page.objects.live().in_menu().public().filter(locale=locale)
    }
