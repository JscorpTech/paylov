from rest_framework import serializers

from core.apps.api.models import OrderitemsModel


class BaseOrderitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderitemsModel
        fields = [
            "id",
            "name",
        ]


class ListOrderitemsSerializer(BaseOrderitemsSerializer):
    class Meta(BaseOrderitemsSerializer.Meta): ...


class RetrieveOrderitemsSerializer(BaseOrderitemsSerializer):
    class Meta(BaseOrderitemsSerializer.Meta): ...


class CreateOrderitemsSerializer(BaseOrderitemsSerializer):
    class Meta(BaseOrderitemsSerializer.Meta):
        fields = [
            "id",
            "name",
        ]
