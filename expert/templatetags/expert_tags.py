from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def expert_link(expert):
    return f'<a href="{expert.get_absolute_url()}" target="_blank">{expert.name}</a>'


@register.simple_tag
def format_connections(connections, term):
    result = []
    for connection in connections:
        person = connection[-1]
        headers = [header.replace('<br/>', '') for header in person.heading_text.split('\n') if term in header]
        headers = '|'.join(headers)
        people = ' > '.join([expert_link(expert) for expert in connection])
        result.append(people + ' (' + headers + ')')
    result = ''.join(['<li>' + item + '</li>' for item in result])
    return mark_safe(result)
