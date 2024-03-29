from pyexpat import model
from tkinter import CASCADE
from django.db import models
from uuid import uuid4
from django.conf import settings
from core.models import CustomUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# from django_resized import ResizedImageField
User=get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+',default="",blank=True)

    def __str__(self):
        return self.title
    


class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)


class Product(models.Model):
    TAG_STATUS_NEWEST = 'Newest'
    TAG_STATUS_BEST_SELLER = 'Best Seller'
    TAG_STATUS_MOST_VISITED = 'Most Visited'
    TAG_STATUS_MOST_HIGHEST_QUALITY = 'Highest Quality'
    TAG_STATUS = [
        (TAG_STATUS_NEWEST,'Newest'),
        (TAG_STATUS_BEST_SELLER,'Best Seller'),
        (TAG_STATUS_MOST_VISITED,'Most Visited'),
        (TAG_STATUS_MOST_HIGHEST_QUALITY,'Highest Quality'),
    ]

    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    soled_item=models.IntegerField(default=0,blank=True,null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discounts = models.ManyToManyField(Discount, blank=True)
    # image = models.ForeignKey('ProductImage',on_delete=models.SET_NULL,null=True)
    # image = models.ImageField(upload_to='product_img/', blank=True, null=True, default='')

    top_deal = models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)
    tags=models.CharField(max_length=50, choices=TAG_STATUS, default="",blank=True,null=True)

    def __str__(self):
      return f'{self.id}---{self.name}'

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image=models.ImageField(upload_to='product_img/',null=True,blank=True) 
    # image=ResizedImageField(upload_to='product_img/',default="",null=True,blank="")


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="CustomerUser")
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=255)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(
    # )

    def __str__(self):
        return f'{self.user.first_name} { self.user.last_name}'
    


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True,related_name='Customeraddress')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255,default="")


    def clean(self):
        if len(self.zip_code) < 10:
            raise ValidationError("ZIP code must be 10 characters long.")

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

    RATING_CHOICES=[
        (5,'5'),
        (4,'4'),
        (3,'3'),
        (2,'2'),
        (1,'1'),
    ]

    def get_default_name():
        return settings.AUTH_USER_MODEL.first_name

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commment') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    body = models.TextField(max_length=1000)
    rating = models.IntegerField(choices=RATING_CHOICES,default=4)  # Rating field limited to 1 to 5
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)





  
    def __str__(self):
        return f'{ self.body}'

    

class Cart(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = [['cart', 'product']]


class Ad(models.Model):
    ad_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return f"Ad {self.ad_id} - {self.product}"
