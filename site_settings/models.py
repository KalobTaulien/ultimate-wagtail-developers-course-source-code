from django.db import models

from wagtail.contrib.settings.models import register_setting, BaseGenericSetting, BaseSiteSetting
from wagtail.admin.panels import FieldPanel
from django.core.exceptions import ValidationError


@register_setting
class GenericFooterText(BaseGenericSetting):
    text = models.TextField(blank=True)
    privacy_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('text'),
        FieldPanel('privacy_page'),
    ]


@register_setting
class SocialMediaLinks(BaseSiteSetting):
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    def clean_facebook(self):
        if 'facebook.com/' not in self.facebook:
            raise ValidationError('Facebook URL must contain facebook.com/')
        return self.facebook

    def clean(self):
        super().clean()
        self.clean_facebook()

    panels = [
        FieldPanel('facebook'),
        FieldPanel('twitter'),
        FieldPanel('instagram'),
    ]
