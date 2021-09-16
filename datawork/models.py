from django.db import models
from django.db.models.enums import Choices
from django.shortcuts import reverse
from django.conf import  settings

# Create your models here.
LABEL_CHOICE = (
    ("n","new"),
    ("o","old"),
    ("u","unboxed")
)

STATE_CHOICE = (
    ("BR","Bihar"),
    ("JK","Jharkhand")
)

CITY_CHOICE = (
    ("PUR","Purnea"),
)
ADDRESS_TYPE = (
    ("H","home"),
    ("O","office")
)

class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()

    #slug = puma-jeans-for-men
    #puma jeans for men
    def get_absolute_url(self):
        return reverse("datawork:category",kwargs={'slug': self.slug})

    def __str__(self):
        return  self.title

class Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("datawork:brand", kwargs={'slug': self.slug})

    def __str__(self):
        return self.brand_name


class Item(models.Model):
    title  = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    label = models.CharField(choices=LABEL_CHOICE,max_length=5)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="products/")
    price = models.FloatField()
    discount_price = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("datawork:item",kwargs={
            "slug":self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return  self.item.title

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact= models.CharField(max_length=100)
    pincode = models.IntegerField()
    locality = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    city = models.CharField(choices=CITY_CHOICE,max_length=4)
    state =models.CharField(choices=STATE_CHOICE,max_length=4)
    landmark = models.CharField(max_length=100)
    alternative_no = models.IntegerField(blank=True,null=True)
    address_type = models.CharField(max_length=2,choices=ADDRESS_TYPE)
    default = models.BooleanField(default=False)

    def __str__(self):
        self.user.username


class Payment(models.Model):
    txn_id = models.CharField(max_length=400)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
    code = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=200)
    item = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date  = models.DateTimeField()
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username






