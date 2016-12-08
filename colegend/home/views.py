from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from colegend.components.templatetags.components_tags import DemoComponent
from colegend.core.templatetags.core_tags import link
from colegend.home.models import HomePage

__author__ = 'eraldo'


class PageMixin:
    """
    Tries to find a wagtail cms page and if it finds it, it adds it to the View's context.
    Thus wagtail can relate this view to that page.
    """
    page_class = None
    page_query_kwargs = None

    def get_page_class(self):
        if hasattr(self, 'page_class'):
            return self.page_class
        else:
            raise NotImplementedError(_('PageMixin needs a `page_class` attribute or overwrite `get_page_class`.'))

    def get_page_query_kwargs(self):
        if hasattr(self, 'page_query_kwargs'):
            return self.page_query_kwargs
        else:
            return {}

    def get_page(self):
        page_class = self.get_page_class()
        page_query_kwargs = self.get_page_query_kwargs()
        if page_query_kwargs:
            try:
                return page_class.objects.get(**page_query_kwargs)
            except page_class.DoesNotExist:
                raise page_class.DoesNotExist(
                    '{} object with keyword arguments: {} not found.'.format(page_class.__name__, page_query_kwargs))
        else:
            return page_class.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_page()
        context['page'] = page
        return context


class JoinView(TemplateView):
    template_name = "home/join.html"
