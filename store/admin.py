from django.contrib import admin
from django import forms
from .models import (Product, Category, ProductImage, ProductSpecification, ProductSpecificationValue, ProductType)
from mptt.admin import MPTTModelAdmin
# Register your models here.

admin.site.register(Category, MPTTModelAdmin)
class AdminCategory (admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # it will prepopulate the slug field based on the name field
    
class ProductSpecificationInline (admin.TabularInline):
    model = ProductSpecification
    
class ProductImageInline (admin.TabularInline):
    model = ProductImage

class ProductSpecificationValueInline (admin.TabularInline):
    model = ProductSpecificationValue
    
@admin.register (ProductType)
class AdminProductType (admin.ModelAdmin):
    inlines = [ProductSpecificationInline]


@admin.register(Product)
class AdminProduct (admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSpecificationValueInline]    
    
    
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'slug', 'price', 'in_stock','is_active', 'created', 'updated',]
#     list_filter = ['in_stock', 'is_active']
#     list_editable = ['price', 'in_stock','is_active']
#     prepopulated_fields = {'slug': ('title',)}