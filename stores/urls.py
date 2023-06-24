from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stores/', views.stores, name='stores'),
    path('store/<str:id>/', views.store, name='store'),
    path('category/<str:id>/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('add_to_cart/<str:id>/', views.add_to_cart, name='add_to_cart'),
    path('myCart/', views.myCart, name='myCart'),
    path('manageCart/<str:id>/', views.manageCart, name='manageCart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<str:id>/', views.payment, name='payment'),
    path('<str:ref>', views.verify_payment, name='verify_payment'),
]
