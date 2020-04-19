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
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtailmedia.edit_handlers import MediaChooserPanel
import yarl

from prayer import models as pr_models
from comments import models as com_models


class User(AbstractUser):
    token = models.CharField(max_length=32)
    subscribe_daily_email = models.BooleanField(default=False)

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
    def group_names(self):
        return [g.name for g in self.groups.all()]

    @cached_property
    def is_chatmod(self):
        return self.is_superuser or "chatmod" in [g.name for g in self.groups.all()]

    @cached_property
    def is_pastor(self):
        return "pastor" in self.group_names

    @cached_property
    def is_streamer(self):
        return "streamer" in self.group_names

    def get_next_service_link(self):
        service_page = ServicePage.current_service_page()

        # TODO: get the hostname dynamically
        stream_link = yarl.URL(
            f"https://crossroadsajax.church{service_page.url}"
        ).with_query(dict(mem=self.token))
        return str(stream_link)

    @classmethod
    def get_guest_next_service_link(cls):
        guest = cls.objects.get(username="guest")
        return guest.get_next_service_link()

    def get_services_link(self):
        link = yarl.URL(f"https://crossroadsajax.church/services").with_query(
            dict(mem=self.token)
        )
        return str(link)


@receiver(models.signals.pre_save, sender=User)
def add_token(sender, instance, *args, **kwargs):
    if not instance.token:
        instance.token = secrets.token_hex(8)


class ServiceMediaBlock(AbstractMediaChooserBlock):
    class Meta:
        template = "blocks/service_media_block.html"


class ServicesIndexPage(Page):
    intro = wtfields.RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    @classmethod
    def service_pages(cls):
        return ServicePage.objects.in_menu().order_by("-date")


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


class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        page = ServicePage.current_service_page()
        context["current_service_page"] = page
        return context


class ContentPageMixin:
    @property
    def pagetype(self):
        return self.__class__.__name__

    @property
    def getdescription(self):
        return ""


class ServicePage(Page, ContentPageMixin):
    date = models.DateField("Service date")
    description = wtfields.RichTextField(
        blank=True,
        default="Please join us for our Sunday service as we worship and listen to God's word.",
    )
    stream_link = models.URLField(default="", blank=True)
    chat_enabled = models.BooleanField(default=True)
    weekly_theme = models.CharField(max_length=128, default="", blank=True)

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

    @property
    def getdescription(self):
        return self.description

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("stream_link"),
        FieldPanel("description"),
        InlinePanel("documents", label="Documents"),
        FieldPanel("chat_enabled"),
        StreamFieldPanel("bulletin"),
        FieldPanel("weekly_theme"),
        # StreamFieldPanel("mediasec"),
        # StreamFieldPanel("service"),
    ]

    prayer_requests = models.ManyToManyField(
        pr_models.PrayerRequest, related_name="services_pages"
    )

    def child_pages(self):
        pages = DailyReadingPage.objects.live().descendant_of(self).order_by("-date")
        return pages

    @classmethod
    def current_service_page(cls):
        return cls.objects.all().order_by("date").last()

    def add_prayer_request(self, pr):
        self.prayer_requests.add(pr)

    @property
    def email_attachments(self):
        return [
            doclink.document.file.file
            for doclink in self.documents.all()
            if doclink.include_in_email
        ]

    def get_context(self, request):
        context = super().get_context(request)
        context["self"] = self
        context["prs"] = self.prayer_requests.all()
        context["guest_link"] = User.get_guest_next_service_link()
        return context


class ServicePageDocumentLink(Orderable):
    page = ParentalKey(ServicePage, related_name="documents")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="+")
    include_in_email = models.BooleanField(default=True)

    panels = [
        DocumentChooserPanel("document"),
        FieldPanel("include_in_email"),
    ]


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


class DailyReadingPage(Page, ContentPageMixin):
    date = models.DateField("Date")
    video_link = models.URLField(default="", blank=True)
    content = wtfields.RichTextField(blank=True)
    reflection = wtfields.RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("content"),
        FieldPanel("video_link"),
        FieldPanel("reflection"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        return context

    @cached_property
    def getdescription(self):
        ncomments = com_models.Comment.objects.filter(thread_id=self.pk).count()
        if ncomments > 0:
            return f"{ncomments} comments"
        else:
            return ""
