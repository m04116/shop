from django.contrib import admin
from .models import *


class ProductImageInline(admin.TabularInline):
    """
    Класс добавляет форму в модель в админке. Например в Product
    """
    model = ProductImage
    extra = 0 # не три пустых ряда, я меньше


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields] # генератор для создания списка полей
    inlines = [ProductImageInline] # добавляется форма с картинками в админке

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
