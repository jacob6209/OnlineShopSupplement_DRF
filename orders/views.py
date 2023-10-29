from django.shortcuts import render
from .models import   Order,OrderItem
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .serializers import OrderCreateSerializer,OrderForAdminSerializer,OrderSerializer,OrderUpdateSerializer
from django.shortcuts import redirect

class OrderViewSet(ModelViewSet):
    # permission_classes=[IsAuthenticated]
    http_method_names=['get','post','patch','delete','options','head']
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return[IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method=="POST":
            return OrderCreateSerializer

        if self.request.method=="PATCH":
            return OrderUpdateSerializer
             
        if (self.request.user.is_staff):
            return OrderForAdminSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}

    def create(self, request, *args, **kwargs):
       create_order_serializer= OrderCreateSerializer(data=request.data,
       context={'user_id':self.request.user.id})
       create_order_serializer.is_valid(raise_exception=True)
       create_order=create_order_serializer.save()
       serializers=OrderSerializer(create_order)
       
       return redirect('payment:payment_process', order_id=create_order.id)
    #    return Response(serializers.data)



    def get_queryset(self):
        # return Order.objects.prefetch_related('items__product').all()
        query_set= Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product'),
            )
        ).select_related('customer__user').all()
        user=self.request.user
        if(user.is_staff):
            return query_set
        return query_set.filter(customer__user_id=user.id)

# Create your views here.
