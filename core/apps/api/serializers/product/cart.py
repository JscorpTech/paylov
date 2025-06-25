from rest_framework import serializers

from core.apps.api.models import CartModel
from core.apps.api.serializers.product.product import ListProductSerializer


class BaseCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = ["id", "product", "count"]


class ListCartSerializer(BaseCartSerializer):
    product = ListProductSerializer()

    class Meta(BaseCartSerializer.Meta): ...


class RetrieveCartSerializer(BaseCartSerializer):
    product = ListProductSerializer()

    class Meta(BaseCartSerializer.Meta): ...


class CreateCartSerializer(BaseCartSerializer):
    class Meta(BaseCartSerializer.Meta):
        fields = ["id", "product", "count"]
