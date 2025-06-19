from django_filters import rest_framework as filters

from core.apps.api.models import OrderitemsModel, OrderModel, ProductModel


class ProductFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProductModel
        fields = [
            "name",
        ]


class OrderFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = OrderModel
        fields = [
            "name",
        ]


class OrderitemsFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = OrderitemsModel
        fields = [
            "name",
        ]
