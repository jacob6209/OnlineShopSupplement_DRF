from ast import Delete
from itertools import count, product
from multiprocessing import context
import re
from this import d
from tkinter import NO
from unicodedata import category
from urllib import request
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view ,APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .pagination import DefultPagination
from .models import Address, Cart, CartItem, Category, Customer, Product,Comment
from .serializers import AddItemSerializer, CartItemSerializer, CartSerializer, CategorySerializer, CommentGetSerializer, CommentSerializer, CustomerSerializer, ProductSerializer, UpdateCartItemSerializer
from store import serializers
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from rest_framework.viewsets import ModelViewSet,GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.db.models import Prefetch
from rest_framework.exceptions import PermissionDenied

# class AddressViewSet(ModelViewSet):
#     serializer_class=AddressSerializer
#     queryset=Address.objects.all()


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    # serializer_class=CartItemSerializer
    
    def get_queryset(self):
        cart_pk=self.kwargs['cart_pk']
        return CartItem.objects.select_related("product").filter(cart_id=cart_pk).all()

    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_pk':self.kwargs['cart_pk']}



class CartViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    serializer_class=CartSerializer
    queryset=Cart.objects.prefetch_related('items__product').all()
    # lookup_value_regex='[0-9a-f]{32}'



# class baseView(CBV)
class ProductViewSet(ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['category_id']
    queryset=Product.objects.select_related("category").all()
    pagination_class=DefultPagination
    # pagination_class=PageNumberPagination

    def get_serializer_context(self):
        return {'requesr':self.request}

    def destroy(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        if product.order_items.count()>0:
            return Response({'Error':'Ther Is Some Order Item Inclouding This Product,please Remove Them First'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerViewSet(ModelViewSet):
    permission_classes=[IsAdminUser,]
    serializer_class=CustomerSerializer
    queryset=Customer.objects.all()

    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        user_id=request.user.id
        customer=Customer.objects.get(user_id=user_id)

        if request.method=="GET":
            serializers=CustomerSerializer(customer)
            return Response(serializers.data) 
        elif request.method=="PUT":
            serializers=CustomerSerializer(customer,data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)
        


        # based on mixin 
# class ProductList(ListCreateAPIView):
#     serializer_class=ProductSerializer
#     queryset=Product.objects.select_related("category").all()

#     def get_serializer_context(self):
#         return {'requesr':self.request}

        # onother way using mixinc
    # def get_serializer_class(self):
    #     return ProductSerializer
    # def get_queryset(self):
    #     return Product.objects.select_related("category").all()
   

#-------------------------------------------------  

# class ProductList(APIView):
#     def get(self,request):
#         query=Product.objects.select_related("category").all()
#         serializer=ProductSerializer(query,many=True,context={'request': request})
#         return Response(serializer.data)
#     def post(self,request):
#         serializer=ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response (serializer.data,status=status.HTTP_201_CREATED)


# function Base View
# @api_view(['GET','POST'])
# def Product_list(request):
#     if request.method=='GET':
#         query=Product.objects.select_related("category").all()
#         serializer=ProductSerializer(query,many=True,context={'request': request})
#         return Response(serializer.data)
#     elif request.method=='POST':
#         serializer=ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response (serializer.data,status=status.HTTP_201_CREATED)


#           based on mixin
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class=ProductSerializer
#     queryset=Product.objects.select_related('products').all()

#     def delete(self,request,pk):
#         product=get_object_or_404(Product,pk=pk)
#         if product.order_items.count()>0:
#             return Response({'Error':'Ther Is Some Order Item Inclouding This Product,please Remove Them First'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class based view
# class ProductDetail(APIView):
#     def get(self,request,pk):
#         product=get_object_or_404(Product,pk=pk) 
#         serializer=ProductSerializer(product,context={'request': request})
#         return Response(serializer.data)
    
#     def put(self,request,pk):
#         product=get_object_or_404(Product,pk=pk)
#         serializer=ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)




# @api_view(['GET','PUT','DELETE'])
# def Product_detail(request,pk):
#     product=get_object_or_404(Product,pk=pk)
#     if request.method=="GET":
#         serializer=ProductSerializer(product,context={'request': request})
#         return Response(serializer.data)
#     elif request.method=='PUT':
#         serializer=ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     elif request.method=='DELETE':
#         if product.order_items.count()>0:
#             return Response({'Error':'Ther Is Some Order Item Inclouding This Product,please Remove Them First'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     # try:
#     #     product=Product.objects.get(pk=id)
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)

#     #  if serializer.is_valid():
#     #      serializer.validated_data
#     #      Response("Every thing is ok")
#     #  else:
#     #      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#----------------------------------------------------------------
class CategoryViewSet(ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]
    serializer_class=CategorySerializer
    queryset=Category.objects.prefetch_related('products')

    def destroy(self,request,pk):
        category=get_object_or_404(Category.objects.annotate(
        product_count=Count('products')
        ),pk=pk)
        if category.products.count()>0:
            return Response({'Error':'Ther is Some Product Inclouding This Category,please Remove Them First'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response({'Success':'True'},status=status.HTTP_204_NO_CONTENT) 

#based on Mixin
# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#      serializer_class=CategorySerializer
#      queryset=Category.objects.prefetch_related('products')

#      def delete(self,request,pk):
#         category=get_object_or_404(Category.objects.annotate(
#         product_count=Count('products')
#         ),pk=pk)
#         if category.products.count()>0:
#             return Response({'Error':'Ther is Some Product Inclouding This Category,please Remove Them First'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response({'Success':'True'},status=status.HTTP_204_NO_CONTENT)

# based on class baseView
# class CategoryDetail(APIView):
#     def get(self,request,pk):
#         category=get_object_or_404(Category.objects.prefetch_related('products'),pk=pk)
#         serializers=CategorySerializer(category)
#         return Response(serializers.data)

#     def put(self,request,pk):
#         category=get_object_or_404(Category.objects.prefetch_related('products'),pk=pk)
#         serializers=CategorySerializer(category,data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response({'Success':'True'},status=status.HTTP_200_OK)

#     def delete(self,request,pk):
#         category=get_object_or_404(Category.objects.annotate(
#         product_count=Count('products')
#         ),pk=pk)
#         if category.products.count()>0:
#             return Response({'Error':'Ther is Some Product Inclouding This Category,please Remove Them First'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response({'Success':'True'},status=status.HTTP_204_NO_CONTENT)


# function base view
# @api_view(['GET','PUT','DELETE'])
# def Category_Detail(request,pk):
#     category=get_object_or_404(Category.objects.annotate(
#             product_count=Count('products')
#             ),pk=pk)
#     if request.method=='GET':
#         serializers=CategorySerializer(category)
#         return Response(serializers.data)
#     elif request.method=='PUT':
#         serializers=CategorySerializer(category,data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response({'Success':'True'},status=status.HTTP_200_OK)
#     elif request.method=='DELETE':
#         if category.products.count()>0:
#             return Response({'Error':'Ther is Some Product Inclouding This Category,please Remove Them First'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response({'Success':'True'},status=status.HTTP_204_NO_CONTENT)

#  based on mixin
# class CategoryList(ListCreateAPIView):
#     serializer_class=CategorySerializer
#     queryset=Category.objects.prefetch_related('products').all()
#     def get_serializer_context(self):
#         return {"request":self.request}

# Using ApiView based on View Class
# class CategoryList(APIView):
#     def get(self,request):
#         qry_category=Category.objects.prefetch_related('products').all()
#         serializers=CategorySerializer(qry_category,many=True,context={'request': request})
#         return Response(serializers.data)
    
    # def post(self,request):
    #     serializers=CategorySerializer(data=request.data)
    #     serializers.is_valid(raise_exception=True)
    #     serializers.save()
    #     return Response(serializers.data,status=status.HTTP_201_CREATED)



# @api_view(['GET','POST'])
# def Category_List(request):

#     if request.method=='GET':
#         # qry_category=Category.objects.prefetch_related('products').all() 
#         qry_category=Category.objects.annotate(
#             product_count=Count('products')
#             ).all()
#         serializers=CategorySerializer(qry_category,many=True,context={'request': request})
#         return Response(serializers.data)
#     elif request.method=='POST':
#         serializers=CategorySerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data,status=status.HTTP_201_CREATED)

class CommentViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    
    # serializer_class=CommentSerializer

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.method=="POST":
                if self.request.user.first_name:
                    return CommentGetSerializer
            return CommentSerializer
        else:
            raise PermissionDenied("You must be logged in to post a comment.")
    

    def get_queryset(self):
        product_pk=self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()

    def get_serializer_context(self):
        return  {"product_pk":self.kwargs['product_pk'],"request": self.request}


    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=403)

    

import random
from rest_framework import viewsets
from .models import Ad
from .serializers import adsSerializer

class AdViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = adsSerializer  # Serializer for Ad model

    def get_queryset(self):
        return Ad.objects.all()  # You can customize this queryset further if needed

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        random_ads = random.sample(list(queryset), min(2, len(queryset)))  # Get 2 random ads
        serializer = self.get_serializer(random_ads, many=True)
        return Response(serializer.data)
