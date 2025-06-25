from core.apps.api.models import OrderModel
from django.db import models


def get_order_total_price(order: OrderModel):
    return order.items.annotate(item_price=models.F("price") * models.F("count")).aggregate(
        total_price=models.Sum("item_price")
    )["total_price"]
