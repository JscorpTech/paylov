from rest_framework import serializers

from core.apps.api.models import OrderModel
from core.apps.accounts.serializers.user import UserSerializer


class BaseOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = OrderModel
        fields = [
            "id",
            "user",
        ]


class ListOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta): ...


class RetrieveOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta): ...


class CreateOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta):
        fields = [
            "id",
            "user",
        ]
