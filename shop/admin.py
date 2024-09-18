from django.contrib import admin
from .models import Shop
# Register your models here.


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'owner', 'description', 'phone', 'email',
        'created_at', 'updated_at',
    ]