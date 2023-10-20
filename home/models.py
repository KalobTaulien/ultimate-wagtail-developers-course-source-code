from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model


class HomePage(Page):

    # How to change the template location
    template = "home/home_page.html"
    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model(),  # 'wagtailimages.Image' can be used as a string
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    custom_document = models.ForeignKey(
        get_document_model(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    cta_url = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    cta_external_url = models.URLField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', read_only=True),
        FieldPanel('cta_url'),
        FieldPanel('cta_external_url'),
        FieldPanel('body'),
        FieldPanel('image'),
        FieldPanel('custom_document'),
    ]

    @property
    def get_cta_url(self):
        if self.cta_url:
            return self.cta_url.url
        elif self.cta_external_url:
            return self.cta_external_url
        else:
            return None

    def clean(self):
        super().clean()

        if self.cta_url and self.cta_external_url:
            raise ValidationError({
                'cta_url': 'You can only have one CTA URL',
                'cta_external_url': 'You can only have one CTA URL',
            })
