from django.shortcuts import render
from datawork.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def homepages(req):
    return render(req,"home.html",{
        'categories':Category.objects.all(),
        'products' : Item.objects.all()
    })

def view_product(req,id,slug):
    return render(req,"product.html",{
        'product': Item.objects.get(pk=id),
        'related_products':Item.objects.exclude(pk=id),
    })

def search(req):
    return  render(req,"home.html",{
        'categories': Category.objects.all(),
        'products': Item.objects.filter(title__contains=req.GET.get('search'))
    })

@login_required()
def add_to_cart(req,id):
    pass


def category(req,cat_slug):
    return render(req,"home.html",{
        'categories': Category.objects.all(),
        'products': Item.objects.filter(category__slug=cat_slug)
    })