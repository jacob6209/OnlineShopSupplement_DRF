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
from store.models import Ad, Address, Cart, Category, Customer, Product,Comment,CartItem, ProductImage

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
    # image_url = serializers.SerializerMethodField('get_image_url')   
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]

    # def get_image_url(self, obj):
    #     request = self.context.get('request')
    #     if request is not None:
    #         image_url = request.build_absolute_uri(obj.image.url)
    #         print (image_url)
    #         return image_url
    #     return None

# class CommentGetSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model=Comment
#         fields=["id",'body','rating']
#         ordering = ['datetime_created']

#     def create(self, validated_data):

#         if not self.context['request'].user.is_authenticated:
#             raise PermissionDenied("You must be logged in to post a comment.")
#         product_pk=self.context['product_pk']
#         user = self.context['request'].user

#          # Get the user's first_name and set it as comment's name
#         validated_data['name'] = user.first_name
        
#         # Create a new comment with the obtained name
#         comment = Comment.objects.create(product_id=product_pk, user=user, **validated_data)
#         return comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Comment
        fields=["id",'name','body','rating','datetime_created']
        ordering = ['datetime_created']  

    def create(self, validated_data):
        if not self.context['request'].user.is_authenticated:
            raise PermissionDenied("You must be logged in to post a comment.")
        product_pk=self.context['product_pk']
        user = self.context['request'].user
        name = validated_data.get('name')  # Get the name from the validated data
        user.first_name = name
        user.save()
        
        return Comment.objects.create(product_id=product_pk,user=user,**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField()
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
        fields=['id','title','description','category','category_title','unit_price','slug','inventory','soled_item','tags','price_after_tax','top_deal','flash_sales','images','uploaded_images','comments', 'average_rating']
        read_only_fields = ['slug']  
        
    def get_price_after_tax(self,product:Product):
        return round(product.unit_price*Decimal(1.09),2)

    def get_category_title(self, product: Product):
        return product.category.title

    def get_average_rating(self, obj):
        product_id = obj.id
        average_rating = Comment.objects.filter(product_id=product_id).aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            return round(average_rating, 2)
        else:
             return 4.0

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
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def validate_quantity(self, value):
        if value is None:
            return 1
        return value

    def create(self, validated_data):
        cart_pk = self.context['cart_pk']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        # Ensure quantity is a valid integer, default to 1 if None
        quantity = self.validate_quantity(quantity)

        # Check inventory before adding to cart
        try:
            product_obj = Product.objects.get(id=product.id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'error':'Product not found.'})

        if product_obj.inventory < quantity:
            raise serializers.ValidationError({'error': 'Not enough stock available for this product.'})

        # If CartItem exists, update quantity, else create a new CartItem
        cart_item, created = CartItem.objects.get_or_create(cart_id=cart_pk, product_id=product.id)
        if not created:
            new_quantity = cart_item.quantity + quantity
            if product_obj.inventory >= new_quantity:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                raise serializers.ValidationError({'error': 'Not enough stock available for this product.'})
        else:
            cart_item.quantity = quantity
            cart_item.save()

        self.instance = cart_item
        return cart_item

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class DecreaseCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def validate_quantity(self, value):
        if value is None:
            return 1
        return value

    def update(self, instance, validated_data):
        # Get the quantity from validated_data or use the existing quantity if not provided
        quantity = validated_data.get('quantity', instance.quantity)
        # Ensure the quantity is never less than or equal to 0
        instance.quantity = max(quantity, 0)
        
        instance.quantity -= 1
        if instance.quantity <= 0:
            instance.delete()
        else:
            instance.save()
        return instance
        
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
#------------------------------------------------------

class AdsProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')

class AdsProductSerializer(serializers.ModelSerializer):
    images = AdsProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'images',]

class adsSerializer(serializers.ModelSerializer):
    product=AdsProductSerializer()
    class Meta:
        model=Ad
        fields=['ad_id','product']
#---------------------------------------------------------------------------------
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













 



