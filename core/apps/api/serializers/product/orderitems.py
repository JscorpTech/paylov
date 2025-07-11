from rest_framework import serializers

from core.apps.api.models import OrderitemsModel
from core.apps.api.serializers.product.product import ListProductSerializer


class BaseOrderitemsSerializer(serializers.ModelSerializer):
    product = ListProductSerializer(read_only=True)

    class Meta:
        model = OrderitemsModel
        fields = [
            "id",
            "product",
            "count",
            "price",
            "discount",
        ]


class ListOrderitemsSerializer(BaseOrderitemsSerializer):
    class Meta(BaseOrderitemsSerializer.Meta): ...


class RetrieveOrderitemsSerializer(BaseOrderitemsSerializer):
    class Meta(BaseOrderitemsSerializer.Meta): ...


class CreateOrderitemsSerializer(BaseOrderitemsSerializer):
    product = None

    def create(self, validated_data):
        validated_data["order_id"] = self.context.get("order_id")
        validated_data['price'] = validated_data.get("product")
        raise Exception(validated_data)
        return super().create(validated_data)

    class Meta(BaseOrderitemsSerializer.Meta):
        fields = [
            "id",
            "product",
            "count",
        ]
