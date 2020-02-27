from django import forms
from django.contrib.auth.models import User
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core import fields as wtfields, blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtailmedia.edit_handlers import MediaChooserPanel


class PrayerRequestForm(forms.Form):
    VISIBILITY_CHOICES = [
        ("1", "Only you"),
        ("2", "Only Crossroads members"),
        ("3", "Only Crossroads prayer team members"),
        ("4", "Anyone"),
    ]
    body = forms.CharField(label="Prayer request", max_length=8192, widget=forms.Textarea)
    post_visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES, label="Who can see your submission", initial="2")
    user_visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES, label="Who can see your name", initial="1")


class PrayerRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_visibility = models.IntegerField()
    post_visibility = models.IntegerField()
    body = models.CharField(max_length=8192)


class ServiceMediaBlock(AbstractMediaChooserBlock):
    class Meta:
        template = "blocks/service_media_block.html"


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
    title = blocks.CharBlock()
    speaker = blocks.CharBlock()
    slides_url = blocks.CharBlock()

    class Meta:
        template = "blocks/sermon_section.html"


class DiscussionSectionBlock(blocks.StructBlock):
    class Meta:
        template = "blocks/discussion_section.html"


class ServicePage(Page):
    date = models.DateField("Service date")

    mediasec = wtfields.StreamField([
        ('media', ServiceMediaBlock(icon="media")),
    ])

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
        StreamFieldPanel("mediasec"),
        StreamFieldPanel("bulletin"),
        StreamFieldPanel("service"),
    ]
