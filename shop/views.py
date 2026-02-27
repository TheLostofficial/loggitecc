from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product
from .forms import BrandForm, CategoryForm, FormatForm, ProductForm


def get_user_role(user):
    if not user.is_authenticated:
        return 'guest'
    if user.is_superuser:
        return 'admin'
    return 'user'


def products_page(request):
    user_role = get_user_role(request.user)
    products = Product.objects.select_related('brand', 'category', 'format')

    search = request.GET.get('search', '')
    sort = request.GET.get('sort', 'name-asc')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(brand__name__icontains=search) |
            Q(category__name__icontains=search) |
            Q(description__icontains=search)
        )

    if sort == 'price-asc':
        products = products.order_by('price')
    elif sort == 'price-desc':
        products = products.order_by('-price')
    elif sort == 'name-desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('name')

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'user_role': user_role,
        'search_value': search,
        'sort': sort,
    })


@login_required
def create_view(request, form_class, title, success_msg):
    if not request.user.is_superuser:
        messages.error(request, "Доступ запрещён")
        return redirect('main:products')
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES if 'image' in form_class.Meta.fields else None)
        if form.is_valid():
            form.save()
            messages.success(request, success_msg)
            return redirect('main:products')
    else:
        form = form_class()
    
    return render(request, 'form.html', {'form': form, 'title': title})


@login_required
def update_view(request, pk, model_class, form_class, title, success_msg):
    if not request.user.is_superuser:
        return redirect('main:products')
    
    obj = get_object_or_404(model_class, pk=pk)
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES if 'image' in form_class.Meta.fields else None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, success_msg)
            return redirect('main:products')
    else:
        form = form_class(instance=obj)
    
    return render(request, 'form.html', {'form': form, 'title': title})


def brand_create(request):
    return create_view(request, BrandForm, "Добавить бренд", "Бренд добавлен")


def brand_update(request, pk):
    return update_view(request, pk, Brand, BrandForm, "Редактировать бренд", "Бренд обновлён")


def category_create(request):
    return create_view(request, CategoryForm, "Добавить категорию", "Категория добавлена")


def category_update(request, pk):
    return update_view(request, pk, Category, CategoryForm, "Редактировать категорию", "Категория обновлена")


def format_create(request):
    return create_view(request, FormatForm, "Добавить форму выпуска", "Форма добавлена")


def format_update(request, pk):
    return update_view(request, pk, Format, FormatForm, "Редактировать форму", "Форма обновлена")


def product_create(request):
    return create_view(request, ProductForm, "Добавить продукт", "Продукт добавлен")


def product_update(request, pk):
    return update_view(request, pk, Product, ProductForm, "Редактировать продукт", "Продукт обновлён")
    