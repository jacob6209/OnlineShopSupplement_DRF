from dataclasses import field, fields
from decimal import Decimal, Rounded
from math import fabs
from multiprocessing import context
from pickletools import decimalnl_long
from pyexpat import model
from statistics import mode
# from typing_extensions import Self
from unicodedata import decimal
from urllib import response
from rest_framework  import serializers
from django.utils.text import slugify
from store import models
from django.contrib.auth import get_user_model  
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from django.db.models import Avg
from store.models import Address, Cart, Category, Customer, Product,Comment,CartItem, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    # sub_product=serializers.SerializerMethodField()
    sub_product=serializers.IntegerField(source='products.count',read_only=True)
    class Meta:
        model=Category
        fields=['title','description','sub_product',]

    def get_sub_product(self,category:Category):
        # return category.products.count()
        return category.products.count()
    # title=serializers.CharField(max_length=255)
    # description=serializers.CharField(max_length=255)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Comment
        fields=["id",'name','body','rating']

    def create(self, validated_data):
        if not self.context['request'].user.is_authenticated:
            raise PermissionDenied("You must be logged in to post a comment.")
        product_pk=self.context['product_pk']
        user = self.context['request'].user
        return Comment.objects.create(product_id=product_pk,user=user,**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    images=ProductImageSerializer(many=True,read_only=True)
    title=serializers.CharField(max_length=255,source="name")
    # unit_price=serializers.DecimalField(max_digits=6, decimal_places=2)
    price_after_tax=serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta: 
        model=Product
        # never use all too danger
        # fields="__all__"  #never use all too danger
        fields=['id','title','description','category','unit_price','slug','inventory','price_after_tax','top_deal','flash_sales','images','uploaded_images','comments', 'average_rating']
        read_only_fields = ['slug']  
        
    def get_price_after_tax(self,product:Product):
        return round(product.unit_price*Decimal(1.09),2)


    def get_average_rating(self, obj):
        product_id = obj.id
        average_rating = Comment.objects.filter(product_id=product_id).aggregate(Avg('rating'))['rating__avg']
        return average_rating

    # def create(self, validated_data):
    #     product=Product(**validated_data)
    #     product.slug=slugify(product.name)

    #     uploaded_images = validated_data.pop("uploaded_images")
    #     product = Product.objects.create(**validated_data)
    #     for image in uploaded_images:
    #         ProductImage.objects.create(product=product, image=image)
    #     product.save()
    #     return product

    def create(self, validated_data):
        # product=Product(**validated_data)
        # product.slug=slugify(product.name)
        # product.save()
        # uploaded_images = validated_data.pop("uploaded_images")
        # product = Product.objects.create(**validated_data)
        uploaded_images = validated_data.pop("uploaded_images")
        name = validated_data.get("name")  # Get the name from validated_data
        slug = slugify(name)  # Calculate the slug using the name
        validated_data['slug'] = slug  # Include the slug in validated_data

        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product



class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','unit_price']


class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','product','quantity']

    def validate_quantity(self, value):
        product_id = self.initial_data['product']
        requested_quantity = value

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product not found.')

        if product.inventory < requested_quantity:
            raise serializers.ValidationError('Not enough stock available for this product.')
        return value
    
    def create(self, validated_data):
        cart_pk=self.context['cart_pk']
        product=validated_data.get('product')
        quantity=validated_data.get('quantity')

        # Check inventory before adding to cart
        self.validate_quantity(quantity)

        # if CartItem.objects.filter(cart_id=cart_pk,product_id=product.id).exists():
        try:
            cart_item=CartItem.objects.get(cart_id=cart_pk,product_id=product.id)
            cart_item.quantity +=quantity
            cart_item.save()
        except CartItem.DoesNotExist: 
            cart_item=CartItem.objects.create(cart_id=cart_pk,**validated_data)
        self.instance=cart_item
        return cart_item

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        
class CartItemSerializer(serializers.ModelSerializer):
    product=CartProductSerializer()
    item_total=serializers.SerializerMethodField()

    class Meta:
        model=CartItem
        fields=['id','product','quantity','item_total']

   

    def get_item_total(self,cart_item:CartItem):
        return cart_item.quantity*cart_item.product.unit_price

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField()
    # id=serializers.UUIDField(read_only=True)
    class Meta:
        model=Cart
        fields=["id","items",'total_price']
        read_only_fields=["id"]

    def get_total_price(self,cart:Cart):
        return   sum([item.quantity* item.product.unit_price  for item in cart.items.all()])

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['username','first_name','last_name']
        read_only_fields=['username']

# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Address
#         fields=['province','city','street']

class CustomerSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    # address=AddressSerializer()
    class Meta:
        model=Customer
        fields=['user','phone_number','birth_date']
        read_only_fields=['user']

# class OrderCustomerSerializer(serializers.ModelSerializer):
#     first_name=serializers.CharField(max_length=254,source='user.first_name')
#     last_name=serializers.CharField(max_length=254,source='user.last_name')
#     email=serializers.CharField(max_length=254,source='user.email')
#     class Meta:
#         model=Customer
#         fields=['id','first_name','last_name','email']



# class OrderItemProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Product
#         fields=['id','name','unit_price']

# class OrderItemSerializer(serializers.ModelSerializer):
#     product=OrderItemProductSerializer()
#     class Meta:
#         model=OrderItem
#         fields=['id','product','quantity','unit_price']

# class OrderSerializer(serializers.ModelSerializer):
#     items=OrderItemSerializer(many=True)

#     class Meta:
#         model=Order
#         fields=['id','status','datetime_created','items']

# class OrderForAdminSerializer(serializers.ModelSerializer):
#     items=OrderItemSerializer(many=True)
#     customer=OrderCustomerSerializer()

#     class Meta:
#         model=Order
#         fields=['id','customer','status','datetime_created','items']

# class OrderUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Order
#         fields=['status']


# class OrderCreateSerializer(serializers.Serializer):
#     cart_id=serializers.UUIDField()

#               # 2 Solostion
#     # try:
#     #     if Cart.objects.prefetch_related('items').get(id=cart_id).items.count()==0:
#     #         raise serializers.ValidationError("There Is No Cart With Cart Id")
#     # except Cart.DoesNotExist:
#     #        raise serializers.ValidationError("Your Cart is Empty,Please Add Some Product First")
      
#               # 1 solotion  
#     def validate_cart_id(self,cart_id):
#         if not Cart.objects.filter(id=cart_id).exists():
#             return serializers.ValidationError("There Is No Cart With Cart Id")

#         if (CartItem.objects.filter(cart_id=cart_id).count()==0):
#             return serializers.ValidationError("Your Cart is Empty,Please Add Some Product First")
#         return cart_id




#     def save(self, **kwargs):
#         with transaction.atomic():
#             cart_id=self.validated_data['cart_id']
#             user_id=self.context['user_id']
#             customer=Customer.objects.get(user_id=user_id)

#             order=Order()
#             order.customer=customer 
#             order.save()
#             cart_items=CartItem.objects.select_related('product').filter(cart_id=cart_id)
                
#                 # using list conpention
#             order_items=[
#                 OrderItem(
#                     order=order,
#                     product=cart_item.product,
#                     unit_price=cart_item.product.unit_price,
#                     quantity=cart_item.quantity
#                 ) for cart_item in cart_items
#             ]
#                 # Secent Solotion
#             # order_items=list()
#             # for cart_item in cart_items:
#             #     order_item=OrderItem()
#             #     order_item.order=order
#             #     order_item.product_id=cart_item.product_id
#             #     order_item.unit_price=cart_item.product.unit_price
#             #     order_item.quantity=cart_item.quantity
#             # order_items.append(order_item)

#             OrderItem.objects.bulk_create(order_items)
#             Cart.objects.get(id=cart_id).delete()
#             return order













 



