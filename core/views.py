from django.shortcuts import render
from .models import Item

def products(request):
    context={
        'items':Item.objects.all()
    }
    return render(request,"product-page.html",context)

def checkout(request):
    return render(request,"checkout-page.html")

def home(request):
    context={
        'items':Item.objects.all()
    }
    return render(request,"home-page.html",context)