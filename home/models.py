from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, FieldRowPanel, HelpPanel, MultipleChooserPanel, TitleFieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model

from modelcluster.fields import ParentalKey


# An Orderable is a model that can be added to another model via an InlinePanel
# This allows you to add multiple objects to a model.
class HomePageGalleryImage(Orderable):
    # ParentalKey connects this model to it's parent model (HomePage)
    page = ParentalKey(
        'home.HomePage',
        related_name='gallery_images', # The related name is used in the InlinePanel
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(      # A standard ForeignKey
        get_image_model(),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='+',
    )
    # ...
    # You can add additional fields here as well.


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
        # Title Field Example
        TitleFieldPanel(
            'subtitle',
            help_text='The subtitle will appear below the title',
            placeholder='Enter your subtitle',
        ),
        # Inline / Orderable Example #1
        InlinePanel(
            'gallery_images',
            label="Gallery images",
            min_num=2,
            max_num=4,
        ),
        # Inline / Orderable Example #1
        # MultipleChooserPanel(
        #     'gallery_images',       # Links to HomePageGalleryImage.page (ParentalKey)
        #     label="Gallery images",
        #     min_num=2,
        #     max_num=4,
        #     chooser_field_name="image", # Uses the `image` field on HomePageGalleryImage
        #     icon='code',
        # ),
        # MultiFieldPanel Example
        # Takes a List of Panels to group together from top to bottom. Can be nested.
        MultiFieldPanel(
            [
                # HelpPanel Example
                # First item in the MultiFieldPanel
                HelpPanel(
                    content="<strong>Help Panel</strong><p>Help text goes here</p>",
                    heading="Note:",
                ),
                # FieldRowPanel Example
                # Second item in the MultiFieldPanel. Takes a List of Panels to group together from side to side.
                FieldRowPanel(
                    [
                        # PageChooserPanel Example
                        # First item in the FieldRowPanel
                        PageChooserPanel(
                            'cta_url',
                            'blogpages.BlogDetail',
                            help_text='Select the approriate blog page',
                            heading='Blog Page Selection',
                            classname="col6"
                        ),
                        # Standard FieldPanel Example
                        # Second item in the FieldRowPanel
                        FieldPanel(
                            'cta_external_url',
                            help_text='Enter the external URL',
                            heading='External URL',
                            classname="col6"
                        ),
                    ],
                    help_text="Select a page or enter a URL",
                    heading="Call to action URLs"
                ),
            ],
            heading="MultiFieldPanel Demo",
            # classname="collapsed",
            help_text='Random help text',
        )
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
