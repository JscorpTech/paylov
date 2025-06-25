from rest_framework import serializers

from core.apps.api.models import ProductModel
from core.apps.api.models.product import CartModel


class BaseProductSerializer(serializers.ModelSerializer):
    is_basket = serializers.SerializerMethodField()

    def get_is_basket(self, obj) -> bool:
        request = self.context.get("request")
        if request is None:
            return False
        user = request.user
        if not user.is_authenticated:
            return False
        return CartModel.objects.filter(product=obj, user=user).exists()

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "name",
            "price",
            "quantity",
            "image",
            "description",
            "is_basket",
        ]


class ListProductSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta): ...


class RetrieveProductSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta): ...


class CreateProductSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        fields = [
            "id",
            "name",
            "price",
            "quantity",
            "image",
            "description",
        ]
