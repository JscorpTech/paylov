from rest_framework import serializers

from core.apps.api.models import ProductModel
from core.apps.api.models.product import CartModel
from core.apps.shared.utils import get_exchange_rate
from django_core.serializers import AbstractTranslatedSerializer


class PriceSerializer(serializers.Serializer):
    usd = serializers.SerializerMethodField()
    uzs = serializers.SerializerMethodField()

    def get_usd(self, price):
        exchange_rate = get_exchange_rate()
        price_usd = price / exchange_rate
        return round(price_usd, 2)

    def get_uzs(self, price):
        return price


class BaseProductSerializer(AbstractTranslatedSerializer):
    is_basket = serializers.SerializerMethodField()
    price = PriceSerializer()

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
        translated = 0
        translated_fields = [
            "name",
            "description",
        ]
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
