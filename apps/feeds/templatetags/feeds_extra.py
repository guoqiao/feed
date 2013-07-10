# -*- coding: utf-8 -*-
from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.inclusion_tag('feeds/feed_btns.html',takes_context=True)
def feed_btns(context,feed):
    user = context['user']
    return {'feed':feed,'user':user}

@register.filter
@stringfilter
def shortzh(value, arg):
    """
    Truncates a string after a certain number of words including
    alphanumeric and CJK characters.
    Argument: Number of words to truncate after.
    """
    try:
        bits = []
        for x in arg.split(u':'):
            if len(x) == 0:
                bits.append(None)
            else:
                bits.append(int(x))
        if int(x) < len(value):
            return value[slice(*bits)] + '...'
        return value[slice(*bits)]

    except (ValueError, TypeError):
        return value # Fail silently.

