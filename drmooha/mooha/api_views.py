from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Tag, Product, Order, OrderItem, Cart, CartItem
from .serializers import (
    CategorySerializer, TagSerializer, ProductSerializer,
    OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Администратор').exists()

class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name__in=['Продавец', 'Администратор']).exists()

class IsAdminOrSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name__in=['Продавец', 'Администратор']).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.groups.filter(name='Администратор').exists():
            return True
        if request.user.groups.filter(name='Продавец').exists():
            if request.method == 'DELETE':
                obj.is_deleted = True
                obj.save()
                return False
            return True
        return False

@method_decorator(login_required, name='dispatch')
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с категориями товаров.
    
    list:
    Возвращает список всех категорий.
    
    create:
    Создает новую категорию (только для администраторов).
    
    retrieve:
    Возвращает информацию о конкретной категории.
    
    update:
    Обновляет информацию о категории (только для администраторов).
    
    destroy:
    Удаляет категорию (только для администраторов).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

@method_decorator(login_required, name='dispatch')
class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с тегами товаров.
    
    list:
    Возвращает список всех тегов.
    
    create:
    Создает новый тег (только для администраторов).
    
    retrieve:
    Возвращает информацию о конкретном теге.
    
    update:
    Обновляет информацию о теге (только для администраторов).
    
    destroy:
    Удаляет тег (только для администраторов).
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]

@method_decorator(login_required, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с товарами.
    
    list:
    Возвращает список всех товаров.
    
    create:
    Создает новый товар (только для продавцов и администраторов).
    
    retrieve:
    Возвращает информацию о конкретном товаре.
    
    update:
    Обновляет информацию о товаре (только для продавцов и администраторов).
    
    destroy:
    Логически удаляет товар (только для продавцов и администраторов).
    """
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrSellerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Восстанавливает логически удаленный товар",
        responses={
            200: openapi.Response(
                description="Товар успешно восстановлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Статус операции')
                    }
                )
            )
        }
    )
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        if not request.user.groups.filter(name__in=['Продавец', 'Администратор']).exists():
            return Response({'error': 'У вас нет прав для восстановления товара'}, status=403)
        product = self.get_object()
        product.is_deleted = False
        product.save()
        return Response({'status': 'product restored'})

@method_decorator(login_required, name='dispatch')
class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с заказами.
    
    list:
    Возвращает список всех заказов.
    
    create:
    Создает новый заказ.
    
    retrieve:
    Возвращает информацию о конкретном заказе.
    
    update:
    Обновляет информацию о заказе (только для продавцов и администраторов).
    
    destroy:
    Удаляет заказ (только для продавцов и администраторов).
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsSellerOrReadOnly]

@method_decorator(login_required, name='dispatch')
class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с корзиной пользователя.
    
    list:
    Возвращает корзину текущего пользователя.
    
    create:
    Создает новую корзину для текущего пользователя.
    
    retrieve:
    Возвращает информацию о корзине текущего пользователя.
    
    update:
    Обновляет информацию о корзине текущего пользователя.
    
    destroy:
    Удаляет корзину текущего пользователя.
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с товарами в корзине.
    
    list:
    Возвращает список товаров в корзине текущего пользователя.
    
    create:
    Добавляет товар в корзину текущего пользователя.
    
    retrieve:
    Возвращает информацию о конкретном товаре в корзине.
    
    update:
    Обновляет количество товара в корзине.
    
    destroy:
    Удаляет товар из корзины.
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user) 