from django.db import models
from django.conf import settings


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name="Бренд")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField(max_length=255, verbose_name="Форма выпуска")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Форма выпуска"
        verbose_name_plural = "Формы выпуска"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.PositiveIntegerField(default=0, verbose_name="Цена")
    weight = models.CharField(max_length=100, blank=True, verbose_name="Вес / объём")
    servings = models.PositiveIntegerField(null=True, blank=True, verbose_name="Порций")

    image = models.ImageField(
        upload_to='products/images/',
        blank=True,
        null=True,
        verbose_name="Фото"
    )

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name="Бренд")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name="Категория")
    format = models.ForeignKey(Format, on_delete=models.PROTECT, null=True, blank=True, related_name='products', verbose_name="Форма")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} — {self.brand}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} — {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
        