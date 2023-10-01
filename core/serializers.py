import email
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework  import serializers

from store.models import Address,Customer
from store.serializers import UserSerializer

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=['province','city','street']

class CustomerSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    address = AddressSerializer(source='Customeraddress')
    class Meta:
        model=Customer
        fields=['user','phone_number','birth_date','address']
        read_only_fields=['user']
# -------------------------------------------------------------
class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields=['id','username','password','email','first_name','last_name']



class UserSerializer(DjoserUserSerializer):
    customer = CustomerSerializer(source='CustomerUser')
    # phone_number=serializers.CharField(max_length=254,source='CustomerUser.phone_number')
    # birth_date=serializers.CharField(max_length=254,source='CustomerUser.birth_date')
    class Meta(DjoserUserSerializer.Meta):
        fields=['username','email','customer']
    

