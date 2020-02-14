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



class ServicePage(Page):
    date = models.DateField("Service date")

    # body = wtfields.StreamField([
    #     ("bulletin_items", blocks.ListBlock(BulletinItemBlock, label="Bulletin item")),
    # ])

    # Bulletin fields
    # bulletin_kids = wtfields.RichTextField(blank=True)
    # bulletin_library = wtfields.RichTextField(blank=True)
    # bulletin_offering = wtfields.RichTextField(blank=True)
    # bulletin_volunteer_sched = wtfields.RichTextField(blank=True)
    # bulletin_mens = wtfields.RichTextField(blank=True)
    # bulletin_craft = wtfields.RichTextField(blank=True)

    # Worship fields
    # worship_songs = # defined in ServicePageWorshipSong

    # Sermon fields
    # message_name = ...
    # slide_show = ...
    # verses = ... # custom Bible verse loader/picker

    content_panels = Page.content_panels + [
        InlinePanel("bulletin_items", label="Bulletin items"),
        FieldPanel("date"),
        # StreamFieldPanel("body"),
        # InlinePanel("bulletin_items", label="Bulletin items"),
    ]


class ServicePageBulletinItem(Orderable):
    page = ParentalKey(ServicePage, on_delete=models.CASCADE, related_name="bulletin_items")
    title = models.CharField(max_length=250)
    date = models.DateField("Item date")
    contact_name = models.CharField(max_length=250)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    body = wtfields.RichTextField(blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("contact_name"),
        FieldPanel("contact_email"),
        FieldPanel("contact_phone"),
        FieldPanel("body"),
    ]



# class ServicePageWorshipSong(Orderable):
#     page = ParentalKey(ServicePage, on_delete=models.CASCADE, related_name="worship_songs")
#     title = models.CharField(max_length=250)
#     lyrics = wtfields.RichTextField(blank=True)

