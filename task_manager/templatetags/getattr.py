from django import template

register = template.Library()


@register.filter
def getattr(obj, attr_name):
    return obj.__getattribute__(attr_name)
