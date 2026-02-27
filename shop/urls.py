from django.urls import path
from .views import (
    products_page,
    brand_create, brand_update,
    category_create, category_update,
    format_create, format_update,
    product_create, product_update,
)

app_name = 'main'

urlpatterns = [
    path('', products_page, name='products'),
    
    path('brand/create/', brand_create, name='brand_create'),
    path('brand/update/<int:pk>/', brand_update, name='brand_update'),
    
    path('category/create/', category_create, name='category_create'),
    path('category/update/<int:pk>/', category_update, name='category_update'),
    
    path('format/create/', format_create, name='format_create'),
    path('format/update/<int:pk>/', format_update, name='format_update'),
    
    path('product/create/', product_create, name='product_create'),
    path('product/update/<int:pk>/', product_update, name='product_update'),
]
