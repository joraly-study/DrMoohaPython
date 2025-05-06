from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Product, Category, Tag, Order
from .forms import ProductForm, CategoryForm, TagForm, OrderForm

# Create your views here.

TEMPLATE = 'templates/mooha'

def home(request):
    """Начальная страница проекта"""
    return render(request, 'mooha/home.html')

def catalog(request):
    """Страница каталога магазина"""
    return render(request, 'mooha/catalog.html')

def product_add(request):
    """Страница добавления товара"""
    return render(request, 'mooha/product_form.html')

def product_detail(request):
    """Страница вывода товара"""
    return render(request, 'mooha/product_detail.html')

def product_edit(request):
    """Страница изменения товара"""
    return render(request, 'mooha/product_form.html')

def feedback(request):
    """Страница обратной связи"""
    return render(request, 'mooha/feedback.html')

def api_page(request):
    """Страница API"""
    return render(request, 'mooha/api.html')

def profile(request):
    """Страница личного кабинета пользователя"""
    return render(request, 'mooha/profile.html')

def cart(request):
    """Страница корзины"""
    return render(request, 'mooha/cart.html')

class ProductListView(ListView):
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

class ProductDetailView(DetailView):
    model = Product
    template_name = 'mooha/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False)

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'mooha/product_form.html'
    success_url = '/products/'

class CategoryListView(ListView):
    model = Category
    template_name = 'mooha/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'mooha/category_form.html'
    success_url = '/categories/'

class TagListView(ListView):
    model = Tag
    template_name = 'mooha/tag_list.html'
    context_object_name = 'tags'

class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'mooha/tag_form.html'
    success_url = '/tags/'

def product_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    products = Product.objects.filter(tags=tag, is_deleted=False)
    return render(request, 'mooha/product_list.html', {
        'products': products,
        'tag': tag
    })

def product_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_deleted=False)
    return render(request, 'mooha/product_list.html', {
        'products': products,
        'category': category
    })
