from django.contrib import admin
from datawork.models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Coupon)