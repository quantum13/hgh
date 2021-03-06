from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def hero(context, hero):
    return """
        <img src="%(avatar)s" width=18 height=18> <a href="/info/%(login)s">%(login)s <b>[%(level)s]</b></a> <a href="http://github.com/%(login)s"><i>g</i></a>
    """ % {
        'avatar': hero.avatar_url,
        'login': hero.login,
        'level': hero.level,
        }
