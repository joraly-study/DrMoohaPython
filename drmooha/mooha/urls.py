from django.urls import path
from . import views

app_name = 'mooha'

urlpatterns = [
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
]
