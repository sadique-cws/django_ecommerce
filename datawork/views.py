from datawork.models import Category, Item
from django.shortcuts import render
from datawork.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def homepages(req):
    data = {
        "categories" : Category.objects.all(),
        "products" :Item.objects.all()
    }
    return render(req,"home.html",data)


def view(req,id,slug):
    data = {
        'pro': Item.objects.get(pk = id),
        'related_products': Item.objects.exclude(pk=id)
    }
    return render(req,"product_try.html",data)

def search(req):
    data = {
        'categories': Category.objects.all(),
        'products': Item.objects.filter(title__contains = req.GET.get('search'))
    }
    return render(req,"home.html",data)


@login_required
def addToCart(req,id):
    pass

def category(req,cat_slug):
    data = {
        'categories': Category.objects.all(),
        'products': Item.objects.filter(category__slug = cat_slug)
    }

    return render(req,"home.html",data)

