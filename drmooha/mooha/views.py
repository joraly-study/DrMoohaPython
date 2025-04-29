from django.shortcuts import render

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
