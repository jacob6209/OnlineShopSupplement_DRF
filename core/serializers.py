from dataclasses import fields
import email
from pyexpat import model
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework  import serializers

from store.models import Address

class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields=['id','username','password','email','first_name','last_name']

# class CustomerAddressSerializer(serializers.ModelSerializer):
#         class Meta:
#             model=Address
#             fields=['province','city','street']

class UserSerializer(DjoserUserSerializer):
    # customer_address=CustomerAddressSerializer()
    phone_number=serializers.CharField(max_length=254,source='CustomerUser.phone_number')
    birth_date=serializers.CharField(max_length=254,source='CustomerUser.birth_date')
    province=serializers.CharField(max_length=254,source='CustomerUser.Customeraddress.province')
    city=serializers.CharField(max_length=254,source='CustomerUser.Customeraddress.city')
    street=serializers.CharField(max_length=254,source='CustomerUser.Customeraddress.street')
    class Meta(DjoserUserSerializer.Meta):
        fields=['username','email','first_name','last_name','phone_number','birth_date','province','city','street']
    

