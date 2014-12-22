from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'configuration.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # mentor
    url(r'^visions/', include('visions.urls', namespace="visions")),
    url(r'^journal/', include('journals.urls', namespace="journals")),
    url(r'^gatherings/', include('gatherings.urls', namespace="gatherings")),
    url(r'^dojo/', include('dojo.urls', namespace="dojo")),
    url(r'^challenges/', include('challenges.urls', namespace="challenges")),
    # manager
    url(r'^manager/', include('manager.urls', namespace="manager")),
    url(r'^projects/', include('projects.urls', namespace="projects")),
    url(r'^tasks/', include('tasks.urls', namespace="tasks")),
    url(r'^routines/', include('routines.urls', namespace="routines")),
    url(r'^habits/', include('habits.urls', namespace="habits")),
    url(r'^tags/', include('tags.urls', namespace="tags")),
    # motivator
    url(r'^legend/', include('legend.urls', namespace="legend")),
    url(r'^quotes/', include('quotes.urls', namespace="quotes")),
    # operator
    url(r'', include('website.urls')),
    url(r'^features/', include('features.urls', namespace="features")),
    url(r'^news/', include('news.urls', namespace="news")),
    url(r'^tutorials/', include('tutorials.urls', namespace="tutorials")),
    url(r'^contact/', include('contact.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^backend/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    # django-markitup AJAX preview
    url(r'^markitup/', include('markitup.urls')),

    # django-autocomplet-light
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # robots.txt file for crawlers
    (r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# remove group model from admin
from django.contrib.auth.models import Group
admin.site.unregister(Group)
