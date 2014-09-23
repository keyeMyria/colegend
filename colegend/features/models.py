from django.db import models
from django.utils import timezone

__author__ = 'eraldo'


class FeatureManager(models.Manager):
    pass


class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)
    date_published = models.DateField(default=timezone.now)
    MENTOR = 'ME'
    MANAGER = 'MA'
    MOTIVATOR = 'MO'
    OPERATOR = 'OP'
    ROLE_CHOICES = (
        (MENTOR, 'Mentor'),
        (MANAGER, 'Manager'),
        (MOTIVATOR, 'Motivator'),
        (OPERATOR, 'Operator'),
    )
    role = models.CharField(verbose_name="System Role", max_length=2, choices=ROLE_CHOICES, default=OPERATOR)

    objects = FeatureManager()

    class Meta:
        ordering = ["-date_published"]

    def __str__(self):
        return self.name
