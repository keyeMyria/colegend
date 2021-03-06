from django.conf.urls import url
from django.views.generic import RedirectView

from .views import BiographyCreateView, BiographyUpdateView

__author__ = 'eraldo'

app_name = 'biography'
urlpatterns = [
    url(r'^$',
        RedirectView.as_view(url='create/', permanent=False),
        name='index'),
    url(r'^create/$',
        BiographyCreateView.as_view(),
        name='create'),
    url(r'^update/$',
        BiographyUpdateView.as_view(),
        name='update'),
]
