from django.contrib import admin
from Shopping.admin import custom_admin_site
from django.utils.html import format_html
from django.urls import reverse
from import_export.admin import ExportActionMixin
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)
custom_admin_site.register(Customer)
custom_admin_site.register(Product)
custom_admin_site.register(Cart)
custom_admin_site.register(OrderPlaced)


@admin.register(Customer)
class CustomerModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['id', 'user', 'name',
                    'locality', 'city', 'pincode', 'state']
    list_filter = ('locality', 'pincode',)


@admin.register(Product)
class ProductModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['id', 'title', 'quantity', 'selling_price',
                    'discounted_price', 'get_description', 'brand', 'category', 'product_image']
    list_filter = ('category', 'brand',)

    def get_description(self, obj):
        return obj.description[:20]+'....'
    get_description.short_description = "description"


@admin.register(Cart)
class CartModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['id', 'user', 'product_title', 'quantity']
    list_filter = ('product__title',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def product_title(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['id', 'user', 'customer_id', 'customer_info',
                    'product_info', 'product_id', 'quantity', 'ordered_date', 'status']
    list_filter = ('ordered_date', 'product__title', 'status',)
    readonly_fields = ['id', 'user', 'customer_id', 'customer_info', 'product_info',
                       'product_id', 'quantity', 'ordered_date', 'customer', 'product']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self,  request, obj=None):
        if obj:
            if obj.status=='Delivered':
                return False
            return True

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
