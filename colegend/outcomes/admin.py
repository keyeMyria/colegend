from django.contrib import admin
from .models import Outcome, Step


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ['name', 'scope', 'owner']
    list_filter = ['scope', 'owner', 'tags']
    filter_horizontal = ['tags']


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'outcome']
    # list_filter = ['owner']
