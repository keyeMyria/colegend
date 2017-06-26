from django import template
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import timezone

from colegend.core.utils.markdown import render
from colegend.journals.scopes import Week

register = template.Library()


@register.simple_tag(takes_context=True)
def weekentry_link(context, weekentry=None, **kwargs):
    weekentry = weekentry or context.get('weekentry')
    context = {
        'name': weekentry,
        'url': weekentry.get_absolute_url(),
    }
    context.update(kwargs)
    template = 'weekentries/widgets/link.html'
    return render_to_string(template, context=context)


@register.simple_tag(takes_context=True)
def weekentry_card(context, weekentry=None, **kwargs):
    weekentry = weekentry or context.get('weekentry')
    if weekentry:
        context = {
            'id': weekentry.id,
            'date': weekentry.date,
            'dates': weekentry.dates,
            'week': weekentry,
            'content': render(weekentry.content),
            'actions': True,
            'detail_url': weekentry.detail_url,
            'update_url': weekentry.update_url,
            'delete_url': weekentry.delete_url,
            'keywords': weekentry.keywords,
            'tags': weekentry.tags.all(),
        }
    else:
        context = context.flatten()
        date = kwargs.get('date', context.get('date'))
        if date:
            week = Week(date)
            create_url = reverse('weekentries:create')
            context['create_url'] = '{}?year={}&week={}'.format(create_url, week.start.year, week.number)
            context['dates'] = context.get('dates')
            context['week_number'] = week.number
            context['week'] = week
    context.update(kwargs)
    template = 'weekentries/widgets/card.html'
    return render_to_string(template, context=context)


@register.simple_tag(takes_context=True)
def weekentry_line(context, weekentry=None, **kwargs):
    weekentry = weekentry or context.get('weekentry')
    today = timezone.now().date()
    if weekentry:
        context = {
            'id': weekentry.id,
            'date': weekentry.date,
            'dates': weekentry.dates,
            'week': weekentry,
            'actions': True,
            'detail_url': weekentry.detail_url,
            'update_url': weekentry.update_url,
            'delete_url': weekentry.delete_url,
            'keywords': weekentry.keywords,
            'content': weekentry.content,
            'tags': weekentry.tags.all(),
            'class': 'active' if weekentry.date == today else '',
        }
    else:
        context = context.flatten()
        date = kwargs.get('date', context.get('date'))
        if date:
            week = Week(date)
            create_url = reverse('weekentries:create')
            context['create_url'] = '{}?year={}&week={}'.format(create_url, week.start.year, week.number)
            context['dates'] = '{0} - {1}'.format(week.start, week.end)
            context['week_number'] = week.number
            context['week'] = week
            context['class'] = 'active' if week.date == today else ''
    context.update(kwargs)
    template = 'weekentries/widgets/item.html'
    return render_to_string(template, context=context)
