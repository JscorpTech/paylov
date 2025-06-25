from rest_framework import serializers

from core.apps.api.models import OrderModel
from core.apps.api.serializers.product.orderitems import ListOrderitemsSerializer
from core.apps.api.services import get_order_total_price


class BaseOrderSerializer(serializers.ModelSerializer):
    items = ListOrderitemsSerializer(many=True)
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return get_order_total_price(obj)

    class Meta:
        model = OrderModel
        fields = ["id", "price", "status", "payment_status", "items"]


class ListOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta): ...


class RetrieveOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta): ...


class CreateOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta):
        fields = [
            "id",
            "items",
        ]
