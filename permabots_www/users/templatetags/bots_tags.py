from django import template
from microbot.models import Bot

register = template.Library()

@register.inclusion_tag('bots/menu_bots.html')
def show_menu_bots(user):
    bots = Bot.objects.filter(owner=user)
    return {'bots': bots}