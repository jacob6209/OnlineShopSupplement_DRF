from pyexpat import model
from tkinter import CASCADE
from django.db import models
from uuid import uuid4
from django.conf import settings
from core.models import CustomUser

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title
    


class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discounts = models.ManyToManyField(Discount, blank=True)
    # image = models.ForeignKey('ProductImage',on_delete=models.SET_NULL,null=True)
    # image = models.ImageField(upload_to='product_img/', blank=True, null=True, default='')
    top_deal = models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)

    def __str__(self):
      return f'{self.name}'

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image=models.ImageField(upload_to='product_img/',default="",null=True,blank="")


class Customer(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="CustomerUser")
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(
    # )

    def __str__(self):
        return f'{self.user.first_name} { self.user.last_name}'
    


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True,related_name='Customeraddress')
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

#______________________________________________________ 

# class Order(models.Model):
#     ORDER_STATUS_PAID = 'p'
#     ORDER_STATUS_UNPAID = 'u'
#     ORDER_STATUS_CANCELED = 'c'
#     ORDER_STATUS = [
#         (ORDER_STATUS_PAID,'Paid'),
#         (ORDER_STATUS_UNPAID,'Unpaid'),
#         (ORDER_STATUS_CANCELED,'Canceled'),
#     ]
    
#     customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
#     datetime_created = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
#     quantity = models.PositiveSmallIntegerField()
#     unit_price = models.DecimalField(max_digits=6, decimal_places=2)

#     class Meta:
#         unique_together = [['order', 'product']]

  #______________________________________________________ 


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)


class Cart(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]
