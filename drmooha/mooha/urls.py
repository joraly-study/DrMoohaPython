from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import (
    CategoryViewSet, TagViewSet, ProductViewSet,
    OrderViewSet, CartViewSet, CartItemViewSet
)

app_name = 'mooha'

# Создаем роутер для API
router = DefaultRouter()
router.register(r'api/categories', CategoryViewSet)
router.register(r'api/tags', TagViewSet)
router.register(r'api/products', ProductViewSet)
router.register(r'api/orders', OrderViewSet)
router.register(r'api/cart', CartViewSet, basename='cart')
router.register(r'api/cart-items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    # API маршруты
    path('', include(router.urls)),
    
    # Существующие маршруты
    path('', views.ProductListView.as_view(), name='product_list'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:category_id>/products/', views.product_by_category, name='category_products'),
    
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:tag_id>/products/', views.product_by_tag, name='tag_products'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
