from django.contrib import admin
from .models import (
    Brands, Category, Product, ProductFeature, CategoryFeature,
    ProductComment, ProductTag, ProductGallery, ProductLog,
    Color, Size, Stock
)
from invoice.models import (
Status, Copen, GatewayPayment, Invoice,
    PaymentType, InvoiceItem, InvoiceLog
)


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'logo', 'web_link')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'is_active', 'created', 'updated')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
    'name', 'price', 'off', 'product_stock', 'brands', 'category', 'shop', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('brands', 'category', 'shop', 'is_active')


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'feature', 'feature_value', 'is_active')
    search_fields = ('feature',)


@admin.register(CategoryFeature)
class CategoryFeatureAdmin(admin.ModelAdmin):
    list_display = ('category', 'feature_name', 'slug')
    search_fields = ('feature_name',)


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created', 'is_confirmed')
    search_fields = ('product', 'user')


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('product', 'tag')
    search_fields = ('tag',)


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')


@admin.register(ProductLog)
class ProductLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'action')
    search_fields = ('action',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color_name', 'color_code')
    search_fields = ('color_name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size_name',)
    search_fields = ('size_name',)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size')
    search_fields = ('product', 'color', 'size')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Copen)
class CopenAdmin(admin.ModelAdmin):
    list_display = ('copen_code', 'discount', 'validity', 'until', 'is_active')
    search_fields = ('copen_code',)


@admin.register(GatewayPayment)
class GatewayPaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'created')
    search_fields = ('name',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'total_price', 'created', 'updated')
    search_fields = ('user', 'status')
    list_filter = ('status',)


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'invoice')
    search_fields = ('name',)


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'stock', 'quantity')
    search_fields = ('invoice', 'stock')


@admin.register(InvoiceLog)
class InvoiceLogAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description')
    search_fields = ('invoice', 'description')
