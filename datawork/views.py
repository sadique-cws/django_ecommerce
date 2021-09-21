from typing import OrderedDict
from django.contrib import messages
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.utils import timezone
from datawork.models import *
from datawork.forms import *
import random

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
    

def removeCoupon(req):
    order = Order.objects.filter(user=req.user,ordered=False).first()
    order.coupon = None
    order.save()
    return redirect(cart)



def addCoupon(req):
    if req.method == "POST":
        code = req.POST.get('code')
        checkCode = Coupon.objects.filter(code=code).first()

        if(checkCode):
            order = Order.objects.filter(user=req.user,ordered=False).first()
            order.coupon = checkCode
            order.save()
            messages.success(req,"Coupon applied successfully")
        else:
            messages.error(req,"Coupon invalid or expired")
        
        return redirect(cart)




def cart(req):
    return render(req,"order_summary.html",{
        'pro' : Order.objects.filter(ordered=False, user=req.user).first()
    })
def myOrder(req):
    return render(req,"my_order.html",{
        'order' : Order.objects.filter(ordered=True, user=req.user)
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
                order_item.delete()
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


@login_required()
def singleOrderItemRemove(req,id):
    product  = get_object_or_404(Item,pk=id)

    order = Order.objects.filter(user=req.user,ordered=False).first()
    
    if(order):
        order_item = OrderItem.objects.filter(item=product,ordered=False,user=req.user)[0]
        order.item.remove(order_item)
        order_item.delete()


    return redirect(cart)


def checkout(req):
    form = AddressForm(req.POST or None,use_required_attribute=False)
    order = Order.objects.filter(user=req.user,ordered=False).first()
    if req.method == "POST":
        addressId = req.POST.get("saveAddressId",None)
        if addressId:
            address = Address.objects.get(id=addressId)
            order.address = address
            order.save()
            return redirect(payment)
        else:
            if form.is_valid():
                a = form.save(commit=False)
                a.user = req.user
                a.save()
                order.address = a
                order.save()
                return redirect(payment)
            else:
                return redirect(checkout)

    return render(req,"checkout.html",{
        'form':form,
        'address': Address.objects.filter(user=req.user)
    })

def makeOrder(req):
    order = Order.objects.filter(user=req.user,ordered=False).first()
    random_string = "ORBR0000" + str(random.randint(10000, 99999)) + "IN"
    order.ref_code = random_string
    order.ordered = True

    for oi in order.item.all():
        oi.ordered = True
        oi.save()
    order.save()
    return True       



def payment(req):
    if makeOrder(req):
        return render(req,"payment.html")

def category(req,cat_slug):
    return render(req,"home.html",{
        'categories': Category.objects.all(),
        'products': Item.objects.filter(category__slug=cat_slug)
    })

