from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('feedback/', views.feedback, name='feedback'),
    path('api/', views.api_page, name='api_page'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
]
