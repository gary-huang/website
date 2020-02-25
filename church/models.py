from django import forms
from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core import fields as wtfields, blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtailmedia.edit_handlers import MediaChooserPanel


class PrayerRequestForm(forms.Form):
    VISIBILITY_CHOICES = [
        ("1", "No one (only you)"),
        ("2", "Crossroads members"),
        ("3", "Public"),
    ]
    submitter_visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES, label="Author visibility (who can see your name)", initial="No one (only you)")
    post_visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES, label="Post visibility (who can see your request)", initial="Crossroads members")
    prayer_request = forms.CharField(label="Prayer request", widget=forms.Textarea)


class ServiceMediaBlock(AbstractMediaChooserBlock):
    # def render_basic(self, value, context=None):
    #     if not value:
    #         return ''

    #     if value.type == 'video':
    #         player_code = '''
    #         <div>
    #             <video width="320" height="240" controls>
    #                 {0}
    #                 Your browser does not support the video tag.
    #             </video>
    #         </div>
    #         '''
    #     else:
    #         player_code = '''
    #         <div>
    #             <audio controls>
    #                 {0}
    #                 Your browser does not support the audio element.
    #             </audio>
    #         </div>
    #         '''

    #     return format_html(player_code, format_html_join(
    #         '\n', "<source{0}>",
    #         [[flatatt(s)] for s in value.sources]
    #     ))

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
    pass


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
