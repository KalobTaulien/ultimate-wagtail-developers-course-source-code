from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import Tag

from wagtail import hooks
from wagtail.models import Page
from wagtail.admin.ui.components import Component
from wagtail.admin.site_summary import SummaryItem

from blogpages.models import Author


@register_snippet
class TagSnippetViewSet(SnippetViewSet):
    model = Tag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 200
    list_display = ["name", "slug"]
    search_fields = ("name",)
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]


@register_snippet
class AuthorSnippet(SnippetViewSet):
    model = Author
    add_to_admin_menu = False


@hooks.register('after_publish_page')
def delete_all_cache(request, page):
    cache.clear()



@hooks.register('register_permissions')
def customer_permission_numero_uno():
    return Permission.objects.filter(
        content_type__app_label='blogpages',
        codename='can_edit_author_name'
    )


# Create a custom panel to display on the homepage
class WelcomePanel(Component):
    order = 10
    template_name = "panels/welcome_panel.html"

    # Used to render HTML directly. Not to be used with `template_name` above.
    # def render_html(self, parent_context):
    #     return mark_safe("""
    #        <div style='background-color: black; color: white; padding: 10px'>
    #             <h2 style='color: white'>Welcome to the admin!</h2>
    #             <p style='color: white'>This is a custom panel.</p>
    #         </div>
    #     """)

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['request'] = parent_context['request']
        context['username'] = parent_context['request'].user.username
        return context

    class Media:
        css = {
            'all': ('css/welcome_panel.css', )
        }
        js = ('js/welcome_panel.js', )


# Used to add the WelcomePanel to the homepage
@hooks.register('construct_homepage_panels')
def any_function_name_here(request, panels):
    panels.append(WelcomePanel())


# Create a SummaryItem for purchases
class NewSummaryItem(SummaryItem):
    order = 200
    template_name = "panels/new_summary_item.html"

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['purchases'] = 1000
        return context


# Create a SummaryItem for unpublished pages
class UnpublishedPages(SummaryItem):
    order = 400
    template_name = "panels/unpublished_pages.html"

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['total'] = Page.objects.all().filter(live=False).count()
        return context


# Used to add SumamryItem's to the homepage
@hooks.register('construct_homepage_summary_items')
def summary_items(request, items):
    items.append(
        NewSummaryItem(request)
    )
    items.append(
        UnpublishedPages(request)
    )
