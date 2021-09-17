from django.shortcuts import render
from datawork.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def homepages(req):
<<<<<<< HEAD
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
=======
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

>>>>>>> cda0cd8c226bc20f6785d8983b9833797fb03a20
