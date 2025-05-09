from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Product, Category, Tag, Order, OrderItem, Cart, CartItem
from .forms import ProductForm, CategoryForm, TagForm, OrderForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone

# Create your views here.

TEMPLATE = 'templates/mooha'

@login_required
def home(request):
    """Начальная страница проекта"""
    return render(request, 'mooha/home.html')

@login_required
def catalog(request):
    """Страница каталога магазина"""
    return render(request, 'mooha/catalog.html')

@permission_required('mooha.add_product')
def product_add(request):
    """Страница добавления товара"""
    return render(request, 'mooha/product_form.html')

@login_required
def product_detail(request):
    """Страница вывода товара"""
    return render(request, 'mooha/product_detail.html')

@permission_required('mooha.change_product')
def product_edit(request):
    """Страница изменения товара"""
    return render(request, 'mooha/product_form.html')

@login_required
def feedback(request):
    """Страница обратной связи"""
    return render(request, 'mooha/feedback.html')

@login_required
def api_page(request):
    """Страница API"""
    return render(request, 'mooha/api.html')

@login_required
def profile(request):
    """Страница личного кабинета пользователя"""
    return render(request, 'mooha/profile.html')

@login_required
def cart(request):
    """Страница корзины"""
    return render(request, 'mooha/cart.html')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'mooha/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Товар {product.name} добавлен в корзину')
    return redirect('mooha:cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Товар удален из корзины')
    return redirect('mooha:cart_detail')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('mooha:cart_detail')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.error(request, 'Ваша корзина пуста')
        return redirect('mooha:cart_detail')
    
    if request.method == 'POST':
        order = Order.objects.create(
            order_number=f'ORD-{timezone.now().strftime("%Y%m%d%H%M%S")}',
            delivery_address=request.POST.get('delivery_address'),
            customer_phone=request.POST.get('customer_phone'),
            customer_name=request.POST.get('customer_name')
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        
        cart.delete()
        messages.success(request, 'Заказ успешно оформлен')
        return redirect('mooha:order_detail', order_id=order.id)
    
    return render(request, 'mooha/checkout.html', {'cart': cart})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'mooha/order_detail.html', {'order': order})

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'mooha/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        category_id = self.request.GET.get('category')
        tag_id = self.request.GET.get('tag')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
            
        return queryset

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'mooha/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False)

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'mooha/product_form.html'
    success_url = '/products/'
    permission_required = 'mooha.add_product'

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'mooha/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'mooha/category_form.html'
    success_url = '/categories/'
    permission_required = 'mooha.add_category'

class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'mooha/tag_list.html'
    context_object_name = 'tags'

class TagCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'mooha/tag_form.html'
    success_url = '/tags/'
    permission_required = 'mooha.add_tag'

@login_required
def product_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    products = Product.objects.filter(tags=tag, is_deleted=False)
    return render(request, 'mooha/product_list.html', {
        'products': products,
        'tag': tag
    })

@login_required
def product_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_deleted=False)
    return render(request, 'mooha/product_list.html', {
        'products': products,
        'category': category
    })
