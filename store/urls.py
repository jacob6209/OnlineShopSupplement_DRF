from cgitb import lookup
from email.policy import default
from itertools import product
from django.urls import path
from . import views
from orders.views import OrderViewSet
# from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('categories',views.CategoryViewSet,basename='category')
router.register('cart',views.CartViewSet,basename='cart')
router.register('customers',views.CustomerViewSet,basename='customers')
router.register('orders', OrderViewSet,basename='orders')
router.register('getads',views.AdViewSet,basename='orders')

product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('comments',views.CommentViewSet,basename='product-comment')

cart_items_router=routers.NestedSimpleRouter(router,'cart',lookup='cart')
cart_items_router.register('items',views.CartItemViewSet,basename='cart-items')
urlpatterns =router.urls+product_router.urls+cart_items_router.urls




#  using custom and tridiational method
# urlpatterns = [

#     path("products/",views.ProductList.as_view()), # using Class Base View 
#     # path("products/",views.Product_list), #using fanctional View
#     path('products/<int:pk>/',views.ProductDetail.as_view()),
#     # path('products/<int:pk>/',views.Product_detail),

#     path('category/<int:pk>/',views.CategoryDetail.as_view(),name='category-detail'),
#     # path('category/<int:pk>/',views.Category_Detail,name='category-detail'),
#     path('category/',views.CategoryList.as_view(),name='category-List'),
# ]
