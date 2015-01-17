from django.db import models
from django.utils import timezone
from markitup.fields import MarkupField
from journals.validators import validate_present_or_past
from lib.models import AutoUrlMixin, OwnedBase, TrackedBase, OwnedQueryMixin, ValidateModelMixin, AutoOwnedBase

__author__ = 'eraldo'


class JournalQuerySet(OwnedQueryMixin, models.QuerySet):
    pass


class Journal(AutoOwnedBase, models.Model):
    """
    A django model representing a journal with one entry per day.
    """
    # > owner (pk)
    # > entries
    max_streak = models.IntegerField(default=0)
    topic_of_the_year = models.CharField(max_length=100, blank=True)

    objects = JournalQuerySet.as_manager()

    def __str__(self):
        return "{}'s Journal".format(self.owner)


class DayEntryQuerySet(models.QuerySet):
    def owned_by(self, user):
        return self.filter(journal__owner=user)

    def latest_for(self, user):
        try:
            latest = self.owned_by(user).latest('date')
        except DayEntry.DoesNotExist:
            latest = None
        return latest

    def streak_for(self, user):
        entries = self.owned_by(user)
        dates = entries.dates('date', kind='day', order="DESC")
        today = timezone.datetime.today().date()
        counter = 0
        for date in dates:
            if (today - date).days == counter:
                counter += 1
            else:
                return counter
        # no dates found..
        return counter


class DayEntry(ValidateModelMixin, AutoUrlMixin, TrackedBase, models.Model):
    """
    A django model representing a daily journal entry in text form.
    """
    journal = models.ForeignKey(Journal, related_name="entries")
    date = models.DateField(default=timezone.datetime.today, validators=[validate_present_or_past])
    location = models.CharField(max_length=100)
    focus = models.CharField(max_length=100, help_text="What was the most important experience/topic on this day?")
    content = MarkupField()

    objects = DayEntryQuerySet.as_manager()

    class Meta:
        ordering = ["-date"]
        unique_together = ('journal', 'date')
        verbose_name_plural = "Day Entries"

    def __str__(self):
        return "{}".format(self.date)

    def update_streak(self):
        streak = DayEntry.objects.streak_for(self.journal.owner)
        if streak > self.journal.max_streak:
            self.journal.max_streak = streak
            self.journal.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_streak()
