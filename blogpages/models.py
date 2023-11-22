from django.core.exceptions import ValidationError
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class BlogIndex(Page):

    template = 'blogpages/blog_index_page.html'
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['blogpages.BlogDetail']

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live().public()
        return context


class BlogPageTags(TaggedItemBase):
    content_object = ParentalKey(
        'blogpages.BlogDetail',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )

from blocks import blocks as custom_blocks

class BlogDetail(Page):
    subtitle = models.CharField(max_length=100, blank=True)
    tags = ClusterTaggableManager(through=BlogPageTags, blank=True)

    body = StreamField(
        [
            ('info', custom_blocks.InfoBlock()),
            ('faq', custom_blocks.FAQListBlock()),
            ('text', custom_blocks.TextBlock()),
            ('carousel', custom_blocks.CarouselBlock()),
            ('image', custom_blocks.ImageBlock()),
            ('doc', DocumentChooserBlock(
                group="Standalone blocks"
            )),
            ('page', blocks.PageChooserBlock(
                required=False,
                page_type='home.HomePage',
                group="Standalone blocks"
            )),
            ('author', SnippetChooserBlock('blogpages.Author')),
            ('call_to_action_1', custom_blocks.CallToAction1())
        ],
        block_counts={
            'text': {'min_num': 1},
            'image': {'max_num': 1},
        },
        use_json_field=True,
        blank=True,
        null=True,
    )

    parent_page_types = ['blogpages.BlogIndex']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('subtitle'),
        FieldPanel('tags'),
    ]

    def clean(self):
        super().clean()

        errors = {}

        if 'blog' in self.title.lower():
            errors['title'] = "Title cannot have the word 'Blog'"

        if 'blog' in self.subtitle.lower():
            errors['subtitle'] = "Subtitle cannot have the word 'Blog'"

        if 'blog' in self.slug.lower():
            errors['slug'] = "Slug cannot have the word 'Blog'"

        if errors:
            raise ValidationError(errors)


# Author model for SnippetChooserBlock and ForeignKey's to the Author model.
# Panels go in the SnipeptViewSet in wagtail_hooks.py
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name
