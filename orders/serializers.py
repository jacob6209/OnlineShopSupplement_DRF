
from dataclasses import field, fields
from decimal import Decimal, Rounded
from math import fabs
from multiprocessing import context
from pickletools import decimalnl_long
from pyexpat import model
from statistics import mode
from unicodedata import decimal
from urllib import response
from rest_framework  import serializers
from django.utils.text import slugify
from store.models import Customer,Product,Cart,CartItem
from orders.models import OrderItem,Order
from django.contrib.auth import get_user_model  
from django.db import transaction

class OrderCustomerSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(max_length=254,source='user.first_name')
    last_name=serializers.CharField(max_length=254,source='user.last_name')
    email=serializers.CharField(max_length=254,source='user.email')
    class Meta:
        model=Customer
        fields=['id','first_name','last_name','email']



class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','unit_price']

class OrderItemSerializer(serializers.ModelSerializer):
    product=OrderItemProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)

    class Meta:
        model=Order
        fields=['id','status','datetime_created','items']

class OrderForAdminSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    customer=OrderCustomerSerializer()

    class Meta:
        model=Order
        fields=['id','customer','status','datetime_created','items']

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['status']


class OrderCreateSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()

              # 2 Solostion
    # try:
    #     if Cart.objects.prefetch_related('items').get(id=cart_id).items.count()==0:
    #         raise serializers.ValidationError("There Is No Cart With Cart Id")
    # except Cart.DoesNotExist:
    #        raise serializers.ValidationError("Your Cart is Empty,Please Add Some Product First")
      
              # 1 solotion  
    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            return serializers.ValidationError("There Is No Cart With Cart Id")
        if (CartItem.objects.filter(cart_id=cart_id).count()==0):
            return serializers.ValidationError("Your Cart is Empty,Please Add Some Product First")
        return cart_id



    def save(self, **kwargs):

        with transaction.atomic():
            cart_id=self.validated_data['cart_id']
            user_id=self.context['user_id']
            customer=Customer.objects.get(user_id=user_id)

            order=Order()
            order.customer=customer 
            order.save()
            cart_items=CartItem.objects.select_related('product').filter(cart_id=cart_id)
                
                # using list conpention
            order_items=[
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    unit_price=cart_item.product.unit_price,
                    quantity=cart_item.quantity
                ) for cart_item in cart_items
            ]
                # Secent Solotion
            # order_items=list()
            # for cart_item in cart_items:
            #     order_item=OrderItem()
            #     order_item.order=order
            #     order_item.product_id=cart_item.product_id
            #     order_item.unit_price=cart_item.product.unit_price
            #     order_item.quantity=cart_item.quantity
            # order_items.append(order_item)

            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()
            return order
