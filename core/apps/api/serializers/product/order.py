from rest_framework import serializers

from core.apps.api.models import OrderModel
from core.apps.api.serializers.product.orderitems import ListOrderitemsSerializer


class BaseOrderSerializer(serializers.ModelSerializer):
    items = ListOrderitemsSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ["id", "items"]


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
