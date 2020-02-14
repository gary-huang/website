from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core import fields as wtfields, blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel


class ServicesIndexPage(Page):
    intro = wtfields.RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]



class BulletinItemBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    date = blocks.DateBlock(required=False)
    contact_name = blocks.CharBlock(required=False)
    contact_email = blocks.EmailBlock(required=False)
    contact_phone = blocks.CharBlock(max_length=20, required=False)
    body = blocks.RichTextBlock(blank=True)

    class Meta:
        template = "blocks/bulletin_item.html"


class BulletinSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    items = blocks.ListBlock(BulletinItemBlock, label="Bulletin item")

    class Meta:
        template = "blocks/bulletin_section.html"


class ServicePage(Page):
    date = models.DateField("Service date")

    bulletin = wtfields.StreamField([
        ('bulletin_section', BulletinSectionBlock(name="Bulletin Section")),
    ])

    # Worship fields
    # worship_songs = # defined in ServicePageWorshipSong

    # Sermon fields
    # message_name = ...
    # slide_show = ...
    # verses = ... # custom Bible verse loader/picker

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        StreamFieldPanel("bulletin"),
    ]


# class ServicePageWorshipSong(Orderable):
#     page = ParentalKey(ServicePage, on_delete=models.CASCADE, related_name="worship_songs")
#     title = models.CharField(max_length=250)
#     lyrics = wtfields.RichTextField(blank=True)

