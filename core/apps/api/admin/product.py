from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.api.models import OrderitemsModel, OrderModel, ProductModel


@admin.register(ProductModel)
class ProductAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(OrderModel)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(OrderitemsModel)
class OrderitemsAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
