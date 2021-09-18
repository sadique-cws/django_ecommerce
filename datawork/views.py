from typing import OrderedDict
from django.contrib import messages
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.utils import timezone
from datawork.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def homepage(req):
    return render(req,"home.html",{
        'categories':Category.objects.all(),
        'products' : Item.objects.all()
    })

def view_product(req,id,slug):
    return render(req,"product.html",{
        'product': Item.objects.get(pk=id),
        'related_products':Item.objects.exclude(pk=id),
    })

def cart(req):
    return render(req,"order_summary.html",{
        'products' : Order.objects.filter(ordered=False, user=req.user)
    })
def search(req):
    return  render(req,"home.html",{
        'categories': Category.objects.all(),
        'products': Item.objects.filter(title__contains=req.GET.get('search'))
    })

@login_required()
def addToCart(req,id):
    product = get_object_or_404(Item,pk=id)
    order_item,create = OrderItem.objects.get_or_create(
        item = product,
        user = req.user,
        ordered = False
    )
    order = Order.objects.filter(user=req.user,ordered=False)
    if(order.exists()):
        order = order[0]

        if order.item.filter(item__id=id).exists():
            order_item.qty += 1
            order_item.save()
            messages.success(req,"product updated successfully")
        else:
            order.item.add(order_item)
            messages.success(req,"product added successfully")
    else:
        order = Order.objects.create(
            user=req.user,
            ordered=False,
            ordered_date = timezone.now()
        )
        order.item.add(order_item)
        messages.success(req,"added in cart successfully")
    return redirect(cart)
            # if not exist
@login_required()
def removeFromCart(req,id):
    product = get_object_or_404(Item,pk=id)
    order = Order.objects.filter(user=req.user,ordered=False)
    if(order.exists()):
        order = order[0]
        if order.item.filter(item__id=id).exists():
            order_item = OrderItem.objects.filter(item=product,ordered=False,user=req.user)[0]
            if order_item.qty > 1:
                order_item.qty -= 1
                order_item.save()
                messages.success(req,"product qty updated successfully")
            else:
                order.item.remove(order_item)
                messages.success(req,"product removed successfully")
        else:
            return redirect(cart)
    else:
        order = Order.objects.create(
            user=req.user,
            ordered=False,
            ordered_date = timezone.now()
        )
        order.item.add(order_item)
        messages.success(req,"added in cart successfully")
    return redirect(cart)
            # if not exist

def category(req,cat_slug):
    return render(req,"home.html",{
        'categories': Category.objects.all(),
        'products': Item.objects.filter(category__slug=cat_slug)
    })

