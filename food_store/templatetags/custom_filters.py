from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def format_price(value):
    try:
        value = float(value)
        return "{:,.0f}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value 