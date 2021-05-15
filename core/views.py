from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.contrib import messages


def checkout(request):
    return render(request, "checkout-page.html")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_set = Order.objects.filter(user=request.user, ordered=False)
    if order_set.exists():
        order = order_set[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity updated")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_set = Order.objects.filter(user=request.user, ordered=False)
    if order_set.exists():
        order = order_set[0]
        # if order is already present in cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "No item in your cart")

    return redirect("core:product", slug=slug)
