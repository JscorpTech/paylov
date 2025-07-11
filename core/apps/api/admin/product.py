from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from core.apps.api.models import CartModel, OrderitemsModel, OrderModel, ProductModel
from unfold.decorators import display
from core.apps.api.enums import OrderStatusEnum, PaymentStatusEnum
from modeltranslation.admin import TabbedTranslationAdmin


class OrderItemInline(TabularInline):
    model = OrderitemsModel
    tab = True
    extra = 0

@admin.register(ProductModel)
class ProductAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ("id", "name", "price", "quantity")


@admin.register(OrderModel)
class OrderAdmin(ModelAdmin):
    inlines = [OrderItemInline]
    list_display = (
        "id",
        "user__phone",
        "user__first_name",
        "_status",
        "_payment_status",
        "created_at",
        "updated_at",
    )

    @display(
        description="payment status",
        ordering="payment_status",
        label={
            PaymentStatusEnum.PENDING.value: "warning",
            PaymentStatusEnum.CANCELED.value: "danger",
            PaymentStatusEnum.PAID.value: "success",
        },
    )
    def _payment_status(self, obj):
        return obj.payment_status

    @display(
        description="status",
        ordering="status",
        label={
            OrderStatusEnum.CREATED.value: "info",
            OrderStatusEnum.CANCELED.value: "danger",
            OrderStatusEnum.DELIVERED.value: "success",
        },
    )
    def _status(self, obj):
        return obj.status


@admin.register(OrderitemsModel)
class OrderitemsAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(CartModel)
class CartAdmin(ModelAdmin):
    list_display = (
        "id",
        "product__name",
        "user__phone",
        "created_at",
        "updated_at",
    )
