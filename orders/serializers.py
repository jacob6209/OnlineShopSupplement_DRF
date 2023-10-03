
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
from core.models import CustomUser
from store.models import Customer,Product,Cart,CartItem,Address
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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('first_name','last_name','phone_number','province', 'city', 'street', 'zip_code')

    def save(self, customer=None, **kwargs):
        address_data = self.validated_data
        address_instance = None
        
        # Check if the address already exists for the given customer
        if customer:
            address_instance = Address.objects.filter(customer=customer).first()

        if address_instance:
            # If address exists, update the fields
            address_instance.first_name = address_data.get('first_name', address_instance.first_name)
            address_instance.last_name = address_data.get('last_name', address_instance.last_name)
            address_instance.phone_number = address_data.get('phone_number', address_instance.phone_number)
            address_instance.province = address_data.get('province', address_instance.province)
            address_instance.city = address_data.get('city', address_instance.city)
            address_instance.street = address_data.get('street', address_instance.street)
            address_instance.zip_code = address_data.get('zip_code', address_instance.zip_code)
            address_instance.save()

            # Update the corresponding Customer fields
            user_instance = customer.user
            user_instance.first_name = address_data.get('first_name', user_instance.first_name)
            user_instance.last_name = address_data.get('last_name', user_instance.last_name)
            user_instance.save()

            customer.phone_number = address_data.get('phone_number', customer.phone_number)
            customer.save()

        else:
            # If address does not exist, create a new address instance and set the customer field
            address_instance = Address(**address_data, customer=customer)
            address_instance.save()

            # Update the corresponding Customer fields
            if customer:
                user_instance = customer.user
                user_instance.first_name = address_data.get('first_name', user_instance.first_name)
                user_instance.last_name = address_data.get('last_name', user_instance.last_name)
                user_instance.save()
                
                customer.phone_number = address_data.get('phone_number', customer.phone_number)
                customer.save()

        return address_instance
    # def save(self, customer=None, **kwargs):
    #     # Check if the customer already has an address
    #     address_instance = customer.Customeraddress if hasattr(customer, 'Customeraddress') else None
       
    #     if customer:
    #         self.validated_data['customer'] = customer
    #     return super().save(**kwargs) 

class OrderCreateSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()
    address = AddressSerializer()  # Use AddressSerializer to handle address fields
    
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
            address_data = self.validated_data['address']  # Get the address from the validated data
            customer=Customer.objects.get(user_id=user_id)


            order=Order()
            order.customer=customer
            order.save()
            cart_items=CartItem.objects.select_related('product').filter(cart_id=cart_id)

            # Validate and create the Address object
            address_serializer = AddressSerializer(data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address_serializer=address_serializer.save(customer=customer)

            # order.Customeraddress = address_instance  # Set the address for the order directly on the customer field
            cart_items=CartItem.objects.select_related('product').filter(cart_id=cart_id)
                
                # using list conpention
            order_items=[
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    unit_price=cart_item.product.unit_price,
                    quantity=cart_item.quantity,

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