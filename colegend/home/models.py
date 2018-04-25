from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
from django.shortcuts import redirect
from django.utils import timezone
from ordered_model.models import OrderedModel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.search import index

from colegend.cms.blocks import BASE_BLOCKS
from colegend.core.fields import MarkdownField
from colegend.core.intuitive_duration.modelfields import IntuitiveDurationField
from colegend.core.models import TimeStampedBase, OwnedBase
from colegend.core.templatetags.core_tags import link

from django.utils.translation import ugettext_lazy as _

from colegend.office.models import AgendaPage
from colegend.scopes.models import ScopeField, get_scope_by_name


class Habit(OwnedBase, TimeStampedBase, OrderedModel):
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    scope = ScopeField()
    icon = models.CharField(
        _('icon'),
        max_length=6,
        blank=True,
    )
    duration = IntuitiveDurationField(
        _('duration'),
        default=timezone.timedelta(minutes=10),
    )
    content = MarkdownField(
        verbose_name=_('content'),
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    is_controlled = models.BooleanField(
        verbose_name=_('controlled'),
        default=False,
        help_text=_(
            'Designates whether this habit is controlled by the system.'
        ),
    )

    def get_stats(self, phases=4):
        """
        Check the last X phases for completion.

        Example:
            Performance of last 4 weeks?
            Result: [0, 1, 1, 0]
            => Not yet a success this week, success the 2 weeks before, no success 3 weeks ago.

        Result type: [{this_phase}, {last_phase}, {pre_last_phase}, {pre_pre_last_phase}]
        """
        # TODO: Refactor to static variables plus updates. (signals?).

        scope = get_scope_by_name(self.scope)()
        stats = [0 for x in range(phases)]  # [0, 0, 0, ...] empty result array

        for phase in range(phases):  # for each phase
            start = scope.start
            end = scope.end
            stats[phase] = self.track_events.filter(created__date__range=(start, end)).count()
            scope = scope.previous

        return stats

    # Reverse: owner, reminders, track_events

    order_with_respect_to = 'owner'

    class Meta(OrderedModel.Meta):
        default_related_name = 'habits'

    def __str__(self):
        return self.name


class HabitTrackEvent(TimeStampedBase):
    habit = models.ForeignKey(
        to=Habit,
        on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'track_events'

    def __str__(self):
        return f'[{self.created}] {self.habit}'


class HabitReminder(TimeStampedBase):
    habit = models.ForeignKey(
        to=Habit,
        on_delete=models.CASCADE
    )

    # Day?: Time
    time = models.TimeField(
        _('time'),
    )

    # Week?: Weekdays
    # monday = models.BooleanField(
    #     verbose_name=_('Monday'),
    #     default=True
    # )
    # tuesday = models.BooleanField(
    #     verbose_name=_('Tuesday'),
    #     default=True
    # )
    # # etc
    # Or: https://github.com/goinnn/django-multiselectfield

    # Alternative: Using CRON syntax?
    # cron = models.CharField(
    #     _('date'),
    # )

    # Month?: Date (on day 21.) | on first/second/etc Weekday
    # date = models.DateField(
    #     _('date'),
    # )

    class Meta:
        default_related_name = 'reminders'

    def __str__(self):
        return f'{self.time}'


class Routine(OwnedBase, TimeStampedBase, OrderedModel):
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    scope = ScopeField()
    content = MarkdownField(
        verbose_name=_('content'),
        blank=True
    )

    # Related reminders
    # TODO: Habits
    habits = models.ManyToManyField(
        to=Habit, through='RoutineHabit')

    # Reverse: owner, reminders

    order_with_respect_to = 'owner'

    class Meta:
        default_related_name = 'routines'

    def __str__(self):
        return self.name


class RoutineHabit(OrderedModel):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    order_with_respect_to = 'routine'

    class Meta:
        ordering = ('routine', 'order')
        default_related_name = 'routine_habits'
        # TODO: Check if unique together is needed here.

    def __str__(self):
        return f'{self.routine}/{self.habit}'


class Scan(OwnedBase, TimeStampedBase):
    date = models.DateField(
        _('date'),
        default=timezone.now
    )
    area_1 = models.PositiveSmallIntegerField(
        _('area 1'),
        validators=[MaxValueValidator(100)]
    )
    area_2 = models.PositiveSmallIntegerField(
        _('area 2'),
        validators=[MaxValueValidator(100)]
    )
    area_3 = models.PositiveSmallIntegerField(
        _('area 3'),
        validators=[MaxValueValidator(100)]
    )
    area_4 = models.PositiveSmallIntegerField(
        _('area 4'),
        validators=[MaxValueValidator(100)]
    )
    area_5 = models.PositiveSmallIntegerField(
        _('area 5'),
        validators=[MaxValueValidator(100)]
    )
    area_6 = models.PositiveSmallIntegerField(
        _('area 6'),
        validators=[MaxValueValidator(100)]
    )
    area_7 = models.PositiveSmallIntegerField(
        _('area 7'),
        validators=[MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = _('scan')
        verbose_name_plural = _('scans')
        default_related_name = 'scans'
        unique_together = ['owner', 'date']
        get_latest_by = 'date'
        ordering = ['-date']

    def __str__(self):
        return 'Scan {0}'.format(self.date)


class HomePage(Page):
    template = 'home/index.html'

    def serve(self, request, *args, **kwargs):
        return redirect(self.get_first_child().url)

    parent_page_types = ['cms.RootPage']
    subpage_types = ['DashboardPage', 'HabitsPage', 'StatsPage']


class DashboardPage(Page):
    template = 'home/dashboard.html'

    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
    ]

    parent_page_types = ['HomePage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['next_step'] = self.get_next_step(request.user)
        return context

    def get_next_step(self, user):
        today = timezone.localtime(timezone.now()).date()

        # Has the user set his focus?
        focus = user.focuses.filter(scope=DAY, start=today)
        agenda_page = AgendaPage.objects.first()
        if not focus and agenda_page:
            url = agenda_page.url + '?scope=day&date={}'.format(today)
            return link(_('Setting focus'), url)

        # Has the user written his journal entry?
        dayentry = user.journal_entries.filter(scope=DAY, start=today)
        if not dayentry:
            return link(_('Create a journal entry'), '#')

    def __str__(self):
        return self.title


class HabitsPage(Page):
    template = 'home/habits.html'

    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
    ]

    parent_page_types = ['HomePage']
    subpage_types = []


class StatsPage(Page):
    template = 'home/stats.html'

    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
    ]

    parent_page_types = ['HomePage']
    subpage_types = []


class JoinPage(Page):
    template = 'home/join.html'

    content = StreamField(BASE_BLOCKS, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = _('Join')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['open'] = True
        if settings.ACCOUNT_ALLOW_REGISTRATION:
            context['open'] = True
        return context
