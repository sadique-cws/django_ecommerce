from datawork.models import Category, Item
from django.shortcuts import render

# Create your views here.
def homepages(req):
    return render(req,"home.html",{
        'categories':Category.objects.all(),
        'products':Item.objects.all(),
        

    })

  