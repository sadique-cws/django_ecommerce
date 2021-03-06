from datawork.views import *
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage,name="home"),
    path('cart/', cart,name="cart"),
    path('checkout/', checkout,name="checkout"),
    path('payment/', payment,name="payment"),
    path('my-order/', myOrder,name="myOrder"),
    path('search/', search,name="search"),
    path('add-coupon/', addCoupon,name="addCoupon"),
    path('remove-coupon/', removeCoupon,name="removeCoupon"),
    path('accounts/', include('allauth.urls')),
    path('add-to-cart/<int:id>/', addToCart,name="addCart"),
    path('remove-from-cart/<int:id>/', removeFromCart,name="removeCart"),
    path('remove-single-from-cart/<int:id>/', singleOrderItemRemove,name="removeSingleCart"),
    path('view/<int:id>/<slug:slug>/', view_product,name="view"),
    path('cat/<slug:cat_slug>/', category,name="category"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
