from datawork.views import *
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepages,name="home"),
    path('search/', search,name="search"),
    path('add-to-cart/<int:id>/', add_to_cart,name="addCart"),
    path('view/<int:id>/<slug:slug>/', view_product,name="view"),
    path('cat/<slug:cat_slug>/', category,name="category"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
