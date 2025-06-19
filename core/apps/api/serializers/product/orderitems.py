from rest_framework import serializers

from core.apps.api.models import OrderitemsModel
from core.apps.api.serializers.product.product import ListProductSerializer
from core.apps.api.serializers.product.order import ListOrderSerializer


class BaseOrderitemsSerializer(serializers.ModelSerializer):
    order = ListOrderSerializer(read_only=True)
    product = ListProductSerializer(read_only=True)

    class Meta:
        model = OrderitemsModel
        fields = [
            "id",
            "order",
            "product",
            "quantity",
            "price",
        ]


class ListOrderitemsSerializer(BaseOrderitemsSerializer):
    class Meta(BaseOrderitemsSerializer.Meta): ...


class RetrieveOrderitemsSerializer(BaseOrderitemsSerializer):
    class Meta(BaseOrderitemsSerializer.Meta): ...


class CreateOrderitemsSerializer(BaseOrderitemsSerializer):
    class Meta(BaseOrderitemsSerializer.Meta):
        fields = [
            "id",
            "order",
            "product",
            "quantity",
            "price",
        ]
