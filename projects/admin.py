from django.contrib import admin
from projects.models import Project

__author__ = 'eraldo'


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    search_fields = ['name']
    list_filter = ['status']
admin.site.register(Project, ProjectAdmin)