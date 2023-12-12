from wagtail.models import Page

def navbar(request):
    return {
        "navbar_pages": Page.objects.live().in_menu().public()
    }
