from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.utils.dateparse import parse_date
from django.db import models
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from colegend.core.fields import MarkdownField
from colegend.core.models import AutoOwnedBase, AutoUrlsMixin, OwnedQuerySet, TimeStampedBase, OwnedBase
from colegend.journals import scopes
from colegend.scopes.models import get_scope_by_name, Scope
from colegend.tags.models import TaggableBase


class JournalEntryQuerySet(models.QuerySet):
    def search(self, query):
        queryset = self.filter(Q(keywords__icontains=query) | Q(content__icontains=query))
        return queryset


class JournalEntry(OwnedBase, TaggableBase, TimeStampedBase):
    """
    A django model representing a user's journal entry.
    """
    scope = models.CharField(
        _('scope'),
        choices=Scope.get_choices(),
        default=Scope.DAY.value,
        max_length=5,
    )
    start = models.DateField(
        _('start'),
    )

    content = MarkdownField(
        _('content'),
        blank=True
    )

    keywords = models.CharField(
        max_length=500,
        help_text="What were the most important experiences/topics?"
    )

    @property
    def end(self):
        return self.get_scope().end

    def get_scope(self):
        return get_scope_by_name(self.scope)(self.start)

    objects = JournalEntryQuerySet.as_manager()

    class Meta:
        verbose_name = _('Journal Entry')
        verbose_name_plural = _('Journal entries')
        unique_together = ['owner', 'scope', 'start']
        ordering = ['-start']
        get_latest_by = 'start'
        default_related_name = 'journal_entries'

    def __str__(self):
        return "{} {}".format(self.get_scope_display(), self.start)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Creation.
            # Adapting start date to scope.
            scope = self.get_scope()
            self.start = scope.start
            # self.end = scope.end
        super().save(*args, **kwargs)


class JournalQuerySet(OwnedQuerySet):
    pass


class Journal(AutoUrlsMixin, AutoOwnedBase):
    """
    A django model representing a user's journal.
    """

    spellchecker = models.BooleanField(default=False)
    day_template = MarkdownField(default=render_to_string('journals/dayentries_template.md'))
    week_template = MarkdownField(default=render_to_string('journals/weekentries_template.md'))
    month_template = MarkdownField(default=render_to_string('journals/monthentries_template.md'))
    year_template = MarkdownField(default=render_to_string('journals/yearentries_template.md'))
    streak = models.PositiveSmallIntegerField(
        _('streak'),
        default=0,
    )
    streak_max = models.PositiveSmallIntegerField(
        _('best streak'),
        default=0,
    )

    objects = JournalQuerySet.as_manager()

    class Meta:
        verbose_name = _('Journal')
        verbose_name_plural = _('Journals')

    def __str__(self):
        return "{}'s journal".format(self.owner)

    @property
    def index_url(self):
        return JournalPage.objects.first().url

    def reset(self):
        self.spellchecker = False
        self.day_template = render_to_string('journals/dayentries_template.md')
        self.week_template = render_to_string('journals/weekentries_template.md')
        self.month_template = render_to_string('journals/monthentries_template.md')
        self.year_template = render_to_string('journals/yearentries_template.md')
        self.save()
        return True


class JournalPage(RoutablePageMixin, Page):
    """
    A journal view with different time scopes.
    """
    template = 'journals/index.html'

    def get_date(self, request):
        date = request.GET.get('date')
        if date:
            return parse_date(date)

    def get_context(self, request, scope, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['scope'] = scope

        date = self.get_date(request) or scope.date
        context['date'] = date

        context['scopes'] = [scope.day, scope.week, scope.month, scope.quarter, scope.year]

        from colegend.journals.forms import DatePickerForm
        context['datepickerform'] = DatePickerForm(initial={'date': date})

        # experience
        context['experience'] = request.user.experience.total(app='studio')
        return context

    def get_date_redirect(self, request, scope):
        # handle date redirect due to get parameter
        get_date = request.GET.get('date')
        if get_date:
            scope.__init__(get_date)
            redirect_url = self.url + self.reverse_subpage(scope.name, kwargs={'date': scope})
            return redirect(redirect_url)

    @route(r'^$')
    @route(r'^(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$')
    def day(self, request, date=None):
        scope = scopes.Day(date)

        date_redirect = self.get_date_redirect(request, scope)
        if date_redirect:
            return date_redirect

        context = self.get_context(request, scope)

        user = request.user
        if user and user.is_authenticated:
            dayentry = user.journal_entries.filter(scope=scope.name, start=scope.start).first()
            context['dayentry'] = dayentry

            outcomes = user.outcomes.all()
            context['scheduled_outcomes'] = outcomes.scheduled(date=scope.date)
            context['deadlined_outcomes'] = outcomes.deadlined(date=scope.date)

        return TemplateResponse(
            request,
            'journals/day.html',
            context
        )

    @route(r'^week/$')
    @route(r'^(?P<date>[0-9]{4}-W[0-9]{2})/$')
    def week(self, request, date=None):
        scope = scopes.Week(date)

        date_redirect = self.get_date_redirect(request, scope)
        if date_redirect:
            return date_redirect

        context = self.get_context(request, scope)

        user = request.user
        if user and user.is_authenticated:
            weekentry = user.journal_entries.filter(scope=scope.name, start=scope.start).first()
            context['weekentry'] = weekentry

            days = []
            day = scopes.Day(scope.start)
            while day.date <= scope.end:
                days.append({
                    'date': day.date,
                    'entry': user.journal_entries.filter(scope=scope.name, start=day.date).first()
                })
                day = day.next
            context['days'] = days

            outcomes = user.outcomes.all()
            start, end = scope.start, scope.end
            context['scheduled_outcomes'] = outcomes.scheduled(date=start, end=end)
            context['deadlined_outcomes'] = outcomes.deadlined(date=start, end=end)

        return TemplateResponse(
            request,
            'journals/week.html',
            context
        )

    @route(r'^month/$')
    @route(r'^(?P<date>[0-9]{4}-M[0-9]{2})/$')
    def month(self, request, date=None):
        scope = scopes.Month(date)

        date_redirect = self.get_date_redirect(request, scope)
        if date_redirect:
            return date_redirect

        context = self.get_context(request, scope)

        user = request.user
        if user and user.is_authenticated:
            monthentry = user.journal_entries.filter(scope=scope.name, year=scope.date.year, month=scope.number).first()
            context['monthentry'] = monthentry

            weeks = []
            week = scopes.Week(scope.start)
            while week.date <= scope.end:
                weeks.append({
                    'date': week.date,
                    'entry': user.journal_entries.filter(scope=week.name, start=week.start).first()
                })
                week = week.next
            context['weeks'] = weeks

            outcomes = user.outcomes.all()
            start, end = scope.start, scope.end
            context['scheduled_outcomes'] = outcomes.scheduled(date=start, end=end)
            context['deadlined_outcomes'] = outcomes.deadlined(date=start, end=end)

        return TemplateResponse(
            request,
            'journals/month.html',
            context
        )

    @route(r'^quarter/$')
    @route(r'^(?P<date>[0-9]{4}-Q[0-4])/$')
    def quarter(self, request, date=None):
        scope = scopes.Quarter(date)

        date_redirect = self.get_date_redirect(request, scope)
        if date_redirect:
            return date_redirect

        context = self.get_context(request, scope)

        user = request.user
        if user and user.is_authenticated:
            quarterentry = user.journal_entries.filter(scope=scope.name, start=scope.start).first()
            context['quarterentry'] = quarterentry

            months = []
            month = scopes.Month(scope.start)
            while month.date <= scope.end:
                months.append({
                    'date': month.date,
                    'entry': user.journal_entries.filter(scope=month.name, start=month.start).first()
                })
                month = month.next
            context['months'] = months

            outcomes = user.outcomes.all()
            start, end = scope.start, scope.end
            context['scheduled_outcomes'] = outcomes.scheduled(date=start, end=end)
            context['deadlined_outcomes'] = outcomes.deadlined(date=start, end=end)

        return TemplateResponse(
            request,
            'journals/quarter.html',
            context
        )

    @route(r'^year/$')
    @route(r'^(?P<date>[0-9]{4})/$')
    def year(self, request, date=None):
        scope = scopes.Year(date)

        date_redirect = self.get_date_redirect(request, scope)
        if date_redirect:
            return date_redirect

        context = self.get_context(request, scope)

        user = request.user
        if user and user.is_authenticated:
            yearentry = user.journal_entries.filter(scope=scope.name, start=scope.start).first()
            context['yearentry'] = yearentry

            quarters = []
            quarter = scopes.Quarter(scope.start)
            while quarter.date <= scope.end:
                quarters.append({
                    'date': quarter.date,
                    'entry': user.journal_entries.filter(scope=quarter.name, start=quarter.start).first()
                })
                quarter = quarter.next
            context['quarters'] = quarters

            outcomes = user.outcomes.all()
            start, end = scope.start, scope.end
            context['scheduled_outcomes'] = outcomes.scheduled(date=start, end=end)
            context['deadlined_outcomes'] = outcomes.deadlined(date=start, end=end)

        return TemplateResponse(
            request,
            'journals/year.html',
            context
        )

    @route(r'^search/$')
    def search(self, request, text=None):
        context = super().get_context(request)
        text = text or request.GET.get('text')
        if text:
            context['text'] = text
            user = request.user
            if user:
                days = user.journal_entries.filter(scope=Scope.DAY.value).filter(
                    Q(keywords__icontains=text) | Q(content__icontains=text) | Q(locations__icontains=text) | Q(
                        tags__name__icontains=text)
                ).distinct()
                context['days'] = days
                weeks = user.journal_entries.filter(scope=Scope.WEEK.value).filter(
                    Q(keywords__icontains=text) | Q(content__icontains=text) | Q(tags__name__icontains=text)
                ).distinct()
                context['weeks'] = weeks
                months = user.journal_entries.filter(scope=Scope.MONTH.value).filter(
                    Q(keywords__icontains=text) | Q(content__icontains=text) | Q(tags__name__icontains=text)
                ).distinct()
                context['months'] = months
                years = user.journal_entries.filter(scope=Scope.YEAR.value).filter(
                    Q(keywords__icontains=text) | Q(content__icontains=text) | Q(tags__name__icontains=text)
                ).distinct()
                context['years'] = years
        return TemplateResponse(
            request,
            'journals/search.html',
            context
        )

    @route(r'^settings/$')
    def settings(self, request):
        from colegend.journals.forms import JournalForm

        context = super().get_context(request)

        user = request.user
        if user:
            journal = user.journal

            # add settings form
            if request.method == 'GET':
                form = JournalForm(instance=journal)
                context['form'] = form

            elif request.method == 'POST':

                # handle reset request
                if request.POST.get('reset'):
                    journal.reset()
                    messages.success(request, _('Journal defaults have been restored.'))
                    return redirect('.')

                # handle posted form
                form = JournalForm(data=request.POST, instance=journal)
                if form.is_valid():
                    form.save()
                    messages.success(request, _('Changes saved.'))
                context['form'] = form

        return TemplateResponse(
            request,
            'journals/settings.html',
            context
        )
