from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModel
from wagtail.core.models import Page

from colegend.categories.models import Category
from colegend.core.fields import MarkdownField
from colegend.core.models import AutoOwnedBase, TimeStampedBase, OwnedBase


class Quest(OrderedModel):
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    video_url = models.URLField(
        _('video url'),
        max_length=1000,
        blank=True
    )
    content = MarkdownField(
        verbose_name=_('content')
    )

    # Reverse: objectives

    # questers = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     through='UserQuestStatus'
    # )

    class Meta(OrderedModel.Meta):
        default_related_name = 'quests'

    def __str__(self):
        return self.name


class QuestObjective(OrderedModel):
    quest = models.ForeignKey(
        to=Quest,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    code = models.CharField(
        _('code'),
        max_length=255,
    )

    order_with_respect_to = 'quest'

    class Meta(OrderedModel.Meta):
        default_related_name = 'objectives'

    def __str__(self):
        return self.name


class UserQuestStatus(OwnedBase, TimeStampedBase):
    quest = models.ForeignKey(
        to=Quest,
        on_delete=models.CASCADE
    )
    completed_objectives = models.ManyToManyField(
        to=QuestObjective,
        blank=True
    )

    class Meta:
        default_related_name = 'quest_statuses'
        unique_together = ['owner', 'quest']
        verbose_name = _("Quest status")
        verbose_name_plural = _("Quest statuses")

    def __str__(self):
        return f'{self.quest} / {self.owner}'


class Hero(AutoOwnedBase, TimeStampedBase):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        blank=True
    )
    avatar = models.URLField(
        _('avatar'),
        max_length=1000,
        blank=True
    )
    year_topic = models.CharField(
        verbose_name=_("year topic"),
        max_length=255,
        blank=True
    )
    vision = MarkdownField(blank=True)
    mission = MarkdownField(blank=True)
    values = MarkdownField(blank=True)
    powers = MarkdownField(blank=True)
    skills = MarkdownField(blank=True)
    habits = MarkdownField(blank=True)
    principles = MarkdownField(blank=True)
    wishes = MarkdownField(blank=True)
    goals = MarkdownField(blank=True)
    people = MarkdownField(blank=True)
    resources = MarkdownField(blank=True)
    achievements = MarkdownField(blank=True)
    questions = MarkdownField(blank=True)
    experiments = MarkdownField(blank=True)
    projects = MarkdownField(blank=True)
    bucket = MarkdownField(blank=True, help_text="bucket list")
    inspirations = MarkdownField(blank=True)
    roles = MarkdownField(blank=True)
    strategy = MarkdownField(blank=True)
    topics = MarkdownField(blank=True)
    routines = MarkdownField(blank=True)
    blueprint_day = MarkdownField(blank=True)
    blueprint_week = MarkdownField(blank=True)
    blueprint_month = MarkdownField(blank=True)
    content = MarkdownField(blank=True)

    class Meta:
        verbose_name = _('Hero')
        verbose_name_plural = _('Heroes')
        default_related_name = 'hero'

    def __str__(self):
        return self.name or f"{self.owner}'s hero"


class Demon(AutoOwnedBase, TimeStampedBase):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        blank=True
    )
    avatar = models.URLField(
        _('avatar'),
        max_length=1000,
        blank=True
    )
    tensions = MarkdownField(blank=True)
    fears = MarkdownField(blank=True)
    content = MarkdownField(blank=True)

    class Meta:
        verbose_name = _('Demon')
        verbose_name_plural = _('Demons')
        default_related_name = 'demon'

    def __str__(self):
        return self.name or f"{self.owner}'s demon"


class QuoteQuerySet(models.QuerySet):
    def accepted(self):
        return self.filter(accepted=True)

    def pending(self):
        return self.filter(accepted=False)

    def random(self):
        return self.accepted().order_by('?').first()

    def owned_by(self, user):
        return self.filter(provider=user)

    def daily_quote(self, date=None):
        # Use only accepted quotes.
        quotes = self.accepted()

        # Fetch past quote if a date was given.
        if date:
            try:
                return quotes.get(used_as_daily=date)
            except Quote.DoesNotExist:
                return None

        # Get or assign today's quote:
        # Check if there already is a quote for today
        # If not..
        # then assign one using a 'new' quote.
        # If there are no new ones..
        # then use the last used quote.

        today = timezone.now().date()
        try:
            current_quote = quotes.get(used_as_daily=today)
        except Quote.DoesNotExist:
            # There is no quote for today yet.. so assign one.
            current_quote = quotes.order_by('used_as_daily').first()
            if current_quote:
                current_quote.used_as_daily = today
                current_quote.save()
        return current_quote


class Quote(TimeStampedBase):
    """A motivational quote."""

    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        unique=True,
        help_text=_("What is the quote about?")
    )
    content = MarkdownField(blank=True)
    author = models.CharField(
        verbose_name=_('author'),
        max_length=255,
        blank=True
    )
    categories = models.ManyToManyField(
        verbose_name=_('categories'),
        to=Category
    )
    provider = models.ForeignKey(
        verbose_name=_('provider'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    accepted = models.BooleanField(
        verbose_name=_('accepted'),
        default=False
    )
    used_as_daily = models.DateField(
        null=True, blank=True,
        unique=True
    )
    liked_by = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='liked_quotes',
        blank=True,
    )
    disliked_by = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='disliked_quotes',
        blank=True,
    )

    objects = QuoteQuerySet.as_manager()

    def __str__(self):
        return self.name

    @property
    def pending(self):
        return not self.accepted

    def accept(self, save=True):
        self.accepted = True
        if save:
            self.save()
        # Notify user
        if self.provider:
            self.provider.contact(subject=f'Your quote "{self.name}" has been accepted. EOM')

    def like(self, user):
        self.disliked_by.remove(user)
        self.liked_by.add(user)

    def dislike(self, user):
        self.liked_by.remove(user)
        self.disliked_by.add(user)

    class Meta:
        default_related_name = 'quotes'


class JourneyPage(Page):
    template = 'journey/base.html'

    def serve(self, request, *args, **kwargs):
        return redirect(self.get_first_child().url)

    parent_page_types = ['cms.RootPage']
    subpage_types = ['QuestPage', 'HeroPage', 'DemonPage', 'AchievementsPage']


class QuestPage(Page):
    template = 'journey/quest.html'

    parent_page_types = ['JourneyPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        user = request.user
        context['experience'] = user.experience.total()
        return context

    def __str__(self):
        return self.title


class HeroPage(Page):
    template = 'journey/hero.html'

    parent_page_types = ['JourneyPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context

    def __str__(self):
        return self.title


class DemonPage(Page):
    template = 'journey/demon.html'

    parent_page_types = ['JourneyPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context

    def __str__(self):
        return self.title


class AchievementsPage(Page):
    template = 'journey/achievements.html'

    parent_page_types = ['JourneyPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context

    def __str__(self):
        return self.title
