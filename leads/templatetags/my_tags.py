from django import template
import random
from django.db.models import Q
register = template.Library()

@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name

@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural

@register.filter
def length(obj):
    return len(obj)

@register.filter
def count(obj):
    count = obj.count()
    return count

@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter
def sum(obj, args):
    value = int(obj)
    number = int(args)
    return value + number

@register.filter
def minus(obj, args):
    value = int(obj)
    number = int(args)
    return value - number

@register.filter
def first_obj(obj):
    return obj.first()

@register.filter
def last_obj(obj):
    return obj.last()

@register.filter
def list(obj, args):
    list = []
    for element in obj:
        if element in args.all():
            list.append(element)
    return list

@register.filter
def section_list(obj, args):
    list = []
    for element in obj:
        if element in args.all():
            list.append(element)
            if len(list) >= 4:
                break
    return list

@register.filter
def reversed(value):
    return value[::-1]