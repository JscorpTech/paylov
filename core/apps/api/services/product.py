from core.apps.api.models import OrderModel
from django.db import models


def get_order_total_price(order: OrderModel):
    return order.items.annotate(item_price=models.F("price") * models.F("count")).aggregate(
        total_price=models.Sum("item_price")
    )["total_price"]


def add_product_quantity_from_order(order):
    for item in order.items.all():
        product = item.product
        count = item.count
        product.quantity += count
        product.save()


def subtrackt_product_quantity_from_order(order):
    for item in order.items.all():
        product = item.product
        count = item.count
        product.quantity -= count
        product.save()