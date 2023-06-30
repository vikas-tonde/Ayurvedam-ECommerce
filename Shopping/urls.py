from django.contrib import admin
from django.urls import path, include
from .admin import custom_admin_site
import app.views as views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    # path('customer', views.customer, name="customer_report"),
    #     path('orderplaced', views.orderplaced, name="orders_report"),
    #     # path('carts', views.carts, name="carts_report"),
    #     path('product', views.product, name="products_report"),
]
