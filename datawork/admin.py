from django.contrib import admin

from datawork.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Address)
admin.site.register(OrderItem)