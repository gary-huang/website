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


class WorshipSongBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    lyrics = blocks.RichTextBlock()

    class Meta:
        template = "blocks/worship_song.html"


class WorshipSectionBlock(blocks.StructBlock):
    worship_songs = blocks.ListBlock(WorshipSongBlock, label="Worship song")

    class Meta:
        template = "blocks/worship_section.html"


class AnnouncementsSectionBlock(blocks.StructBlock):
    pass


class SermonSectionBlock(blocks.StructBlock):
    pass


class ServicePage(Page):
    date = models.DateField("Service date")

    bulletin = wtfields.StreamField([
        ('bulletin_section', BulletinSectionBlock(name="Bulletin Section")),
    ])

    service = wtfields.StreamField([
        ('worship_section', WorshipSectionBlock(name="Worship Section")),
        ('announcements_section', AnnouncementsSectionBlock(name="Announcement Section")),
        ('sermon_section', SermonSectionBlock(name="Sermon Section")),
        # TODO
        # - polls/voting?
        # - feedback
        # - discussion
    ])

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        StreamFieldPanel("bulletin"),
        StreamFieldPanel("service"),
    ]
