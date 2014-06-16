from django.db import models
from status.models import Status

__author__ = 'eraldo'


class Project(models.Model):
    """
    A django model representing a project.
    """
    name = models.CharField(max_length=200, unique=True)

    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, default=Status.objects.default())

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = models.TextField(blank=True)

    def __str__(self):
        return self.name