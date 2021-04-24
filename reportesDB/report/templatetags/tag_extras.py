from django import template

register = template.Library()

@register.simple_tag
def formatDate(date):
    f_date = str(date).split(' ')[0].split('-')
    return f'{f_date[2]}/{f_date[1]}/{f_date[0]}'