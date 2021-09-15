from django.shortcuts import render

# Create your views here.
def homepages(req):
    return render(req,"home.html")