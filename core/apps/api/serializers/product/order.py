from rest_framework import serializers

from core.apps.api.models import OrderModel, OrderitemsModel
from core.apps.api.serializers.product.orderitems import ListOrderitemsSerializer, CreateOrderitemsSerializer
from core.apps.api.services import get_order_total_price
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.transaction import atomic


class BaseOrderSerializer(serializers.ModelSerializer):
    items = ListOrderitemsSerializer(many=True)
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return get_order_total_price(obj)

    class Meta:
        model = OrderModel
        fields = ["id", "price", "status", "payment_status", "is_notify", "items"]


class ListOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta): ...


class RetrieveOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta): ...


class CreateOrderSerializer(BaseOrderSerializer):
    items = CreateOrderitemsSerializer(many=True)

    def validate(self, attrs):
        if not self.context.get("request").user.is_authenticated:
            errors = {}
            if attrs.get("first_name") is None:
                errors["first_name"] = _("First Name is required")
            if attrs.get("last_name") is None:
                errors["last_name"] = _("Last Name is required")
            if attrs.get("phone") is None:
                errors["phone"] = _("Phone is required")
            if attrs.get("address") is None:
                errors["address"] = _("Address is required")
            if len(errors) > 0:
                raise ValidationError(errors)
        return attrs

    def create(self, validated_data):
        items = validated_data.pop("items")
        order = OrderModel.objects.create(**validated_data)
        with atomic():
            for item in items:
                OrderitemsModel.objects.create(order=order, price=item.get("product").price, **item)
        return order

    class Meta(BaseOrderSerializer.Meta):
        fields = [
            "id",
            "items",
            # Order receiver info
            "first_name",
            "last_name",
            "phone",
            "address",
        ]
