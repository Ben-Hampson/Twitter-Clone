from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter
@stringfilter
def hashtags(value):
    sub = re.sub("\B#(\w+)", "<a href='/hashtag/\\1/'>#\\1</a>", value)
    return sub
