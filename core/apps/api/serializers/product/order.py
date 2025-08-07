from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.apps.api.models import OrderModel
from core.apps.api.services import get_order_total_price


class BaseOrderSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return get_order_total_price(obj)

    class Meta:
        model = OrderModel
        fields = [
            "id",
            "price",
            "status",
            "payment_status",
            "is_notify",
            "amount",
        ]


class ListOrderSerializer(BaseOrderSerializer):

    class Meta(BaseOrderSerializer.Meta): ...


class RetrieveOrderSerializer(BaseOrderSerializer):

    class Meta(BaseOrderSerializer.Meta): ...


class CreateOrderSerializer(BaseOrderSerializer):
    # items = CreateOrderitemsSerializer(many=True)
    amount = serializers.IntegerField(required=True)

    def validate(self, attrs):
        if not self.context.get("request").user.is_authenticated:
            errors = {}
            if attrs.get("first_name") is None:
                errors["first_name"] = _("First Name is required")
            if attrs.get("last_name") is None:
                errors["last_name"] = _("Last Name is required")
            if attrs.get("phone") is None:
                errors["phone"] = _("Phone is required")
            if attrs.get("region") is None:
                errors["region"] = _("Region is required")
            if attrs.get("district") is None:
                errors["district"] = _("District is required")
            if attrs.get("company_name") is None:
                errors["company_name"] = _("Company Name is required")
            if attrs.get("city") is None:
                errors["city"] = _("City is required")
            if len(errors) > 0:
                raise ValidationError(errors)
        return attrs

    # def create(self, validated_data):
    #     items = validated_data.pop("items")
    #     order = OrderModel.objects.create(**validated_data)
    #     with atomic():
    #         for item in items:
    #             OrderitemsModel.objects.create(order=order,
    #                                            price=item.get("product").price,
    #                                            **item)
    #     return order

    class Meta(BaseOrderSerializer.Meta):
        fields = [
            "id",
            "amount",
            # "items",
            # Order receiver info
            "first_name",
            "last_name",
            "phone",
            "city",
            "region",
            "district",
            "company_name",
            "comment",
        ]
