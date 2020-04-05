import secrets

from django import forms
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core import fields as wtfields, blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtailmedia.edit_handlers import MediaChooserPanel
import yarl

from prayer import models as pr_models


class User(AbstractUser):
    token = models.CharField(max_length=32)

    # override the username validator
    username_validator = UnicodeUsernameValidator()

    @cached_property
    def role_emoji(self):
        if self.is_superuser:
            return "🛠"
        groups = [g.name for g in self.groups.all()]
        if "pastor" in groups:
            return "😎"
        elif "elder" in groups:
            return "🤓"
        elif "chat_mod" in groups:
            return "🧐"
        return ""

    @cached_property
    def is_chatmod(self):
        return self.is_superuser or "chatmod" in [g.name for g in self.groups.all()]

    def get_next_service_link(self):
        service_page = ServicePage.current_service_page()

        # TODO: get the hostname dynamically
        stream_link = yarl.URL(
            f"https://crossroadsajax.church{service_page.url}"
        ).with_query(dict(mem=self.token))

    @classmethod
    def get_guest_next_service_link(cls):
        guest = cls.objects.get(username="guest")
        return guest.get_next_service_link()


@receiver(models.signals.pre_save, sender=User)
def add_token(sender, instance, *args, **kwargs):
    instance.token = secrets.token_hex(8)


class ServiceMediaBlock(AbstractMediaChooserBlock):
    class Meta:
        template = "blocks/service_media_block.html"


class ServicesIndexPage(Page):
    intro = wtfields.RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    @classmethod
    def service_pages(cls):
        return ServicePage.objects.all().order_by("-date")


class IDListBlock(blocks.ListBlock):
    """Adds an ID to list items. Similarly to what's done
    for structblock children.
    """

    def get_prep_value(self, value):
        r = super().get_prep_value(value)
        for i in r:
            if "id" not in i:
                import uuid

                i["id"] = uuid.uuid4()
        return r


class IDStructBlock(blocks.StructBlock):
    """
    """

    def to_python(self, value):
        self.child_blocks["id"] = blocks.CharBlock(required=False)
        r = super().to_python(value)
        if "id" in value:
            r["id"] = value["id"]
        return r

    def get_prep_value(self, value):
        # TODO: generate an ID here?
        r = super().get_prep_value(value)
        return r


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
    # should be a stream of
    # - polls
    # - discussion

    class Meta:
        template = "blocks/sermon_section.html"


class DiscussionItemBlock(IDStructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock(required=False)

    class Meta:
        template = "blocks/discussion_item_section.html"

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        ctx["item"] = self
        return ctx


class DiscussionSectionBlock(IDStructBlock):
    title = blocks.CharBlock(required=False, default="Discussion")
    items = IDListBlock(DiscussionItemBlock, label="Discussion item")

    class Meta:
        template = "blocks/discussion_section.html"

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        return ctx


class ServicePage(Page):
    date = models.DateField("Service date")
    stream_link = models.URLField(default="", blank=True)
    chat_enabled = models.BooleanField(default=True)

    # mediasec = wtfields.StreamField([
    #     ('media', ServiceMediaBlock(icon="media", required=False)),
    # ])

    bulletin = wtfields.StreamField(
        [("bulletin_section", BulletinSectionBlock(name="Bulletin Section")),],
        blank=True,
    )

    # service = wtfields.StreamField([
    #     ('worship_section', WorshipSectionBlock(name="Worship Section")),
    #     ('announcements_section', AnnouncementsSectionBlock(name="Announcement Section")),
    #     ('sermon_section', SermonSectionBlock(name="Sermon Section")),
    #     ('discussion_section', DiscussionSectionBlock(name="Discussion Section")),
    #     # TODO
    #     # - polls/voting?
    #     # - feedback
    #     # - discussion
    # ])

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("stream_link"),
        FieldPanel("chat_enabled"),
        StreamFieldPanel("bulletin"),
        # StreamFieldPanel("mediasec"),
        # StreamFieldPanel("service"),
    ]

    prayer_requests = models.ManyToManyField(
        pr_models.PrayerRequest, related_name="services_pages"
    )

    @classmethod
    def current_service_page(cls):
        return cls.objects.all().order_by("date").last()

    def add_prayer_request(self, pr):
        self.prayer_requests.add(pr)

    def get_context(self, request):
        context = super().get_context(request)
        context["self"] = self
        context["prs"] = self.prayer_requests.all()
        return context


# class FeaturetteBlock(blocks.StructBlock):
#     pass
#
#
# class ContentPage(Page):
#     content = wtfields.StreamField([
#         ("featurette", FeaturetteBlock(name="Featurettes")),
#     ])
#
#     content_panels = Page.content_panels + [
#         StreamFieldPanel("content"),
#     ]


class OurBeliefsPage(Page):
    pass


class SundayGatheringsPage(Page):
    pass


class PersonalStoriesPage(Page):
    pass
