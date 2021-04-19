from django import template

register = template.Library()

@register.simple_tag
def formatDate(date):
    return str(date).split(' ')[0]