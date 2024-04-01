from django.urls import path
from . import views

urlpatterns = [
    #
    path('', views.home, name='home'),
    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    # product 
    path('productlist', views.productlist, name='productlist'),
    path('createproduct', views.createproduct, name='createproduct'),
    path('productdetails/<int:product_pk>', views.productdetails, name='productdetails'),
    path('productdetails/<int:product_pk>/delete', views.deleteproduct, name='deleteproduct'),
    # order
    path('createorder', views.createorder, name='createorder'),
    path('orderlist/', views.orderlist, name='orderlist'),
    path('orderdetails/<uuid:order_id>/', views.orderdetails, name='orderdetails'),
]