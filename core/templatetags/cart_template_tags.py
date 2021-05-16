from django import template
from core.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        query_set = Order.objects.filter(user=user, ordered=False)
        if query_set.exists():
            return query_set[0].items.count()
    else:
        return 0
