from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.transaction import atomic
from core.apps.api.serializers.product.order import RetrieveOrderSerializer
from core.apps.payment.services import generate_payment_link
from core.apps.api.services import get_order_total_price
from django.db.models import F

from core.apps.api.models import CartModel, OrderitemsModel, OrderModel, ProductModel
from core.apps.api.serializers.product import (
    CreateCartSerializer,
    CreateOrderitemsSerializer,
    CreateOrderSerializer,
    CreateProductSerializer,
    ListCartSerializer,
    ListOrderitemsSerializer,
    ListOrderSerializer,
    ListProductSerializer,
    RetrieveCartSerializer,
    RetrieveOrderitemsSerializer,
    RetrieveOrderSerializer,
    RetrieveProductSerializer,
)


@extend_schema(tags=["product"])
class ProductView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ListProductSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListProductSerializer,
        "retrieve": RetrieveProductSerializer,
        "create": CreateProductSerializer,
    }


@extend_schema(tags=["order"])
class OrderView(BaseViewSetMixin, ReadOnlyModelViewSet):
    serializer_class = ListOrderSerializer
    permission_classes = [IsAuthenticated]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListOrderSerializer,
        "retrieve": RetrieveOrderSerializer,
        "create": CreateOrderSerializer,
    }

    def get_queryset(self):
        queryset = OrderModel.objects.order_by("-id").filter(user=self.request.user)
        if self.action == "notify" or self.action == "notify_read":
            queryset = queryset.filter(is_notify=False)
        return queryset

    @extend_schema(summary="Yangi to'lov qilingan orderlar uchun")
    @action(methods=["GET"], detail=False, url_name="notify", url_path="notify")
    def notify(self, request):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(data={"notify": False})
        return Response(data={"notify": True})

    @extend_schema(summary="Notification o'qildi deb belgilash")
    @action(methods=["GET"], detail=False, url_name="notify-read", url_path="notify-read")
    def notify_read(self, request):
        self.get_queryset().update(is_notify=True)
        return Response(data={"detail": "ok"})

    @extend_schema(summary="Korzonkadagi tovarlarni buyurtma berish")
    @action(methods=["POST"], detail=False, url_name="checkout", url_path="checkout")
    def checkout(self, request):
        carts = self.request.user.carts
        if not carts.exists():
            raise ValidationError(detail={"detail": _("you cart is empty")})
        with atomic():
            order = OrderModel.objects.create(user=request.user)
            for cart in carts.all():
                OrderitemsModel.objects.create(
                    order=order, product=cart.product, count=cart.count, price=cart.product.price
                )
            carts.all().delete()
        link = generate_payment_link(int(get_order_total_price(order)), order.id)
        return Response(
            data={
                "order": RetrieveOrderSerializer(instance=order).data,
                "payment_link": link,
            }
        )

    @extend_schema(summary="Buyurtma uchun to'lov linkini yaratish")
    @action(methods=["GET"], detail=True, url_name="create-transaction", url_path="create-transaction")
    def create_transaction(self, request, pk):
        order = self.get_object()
        link = generate_payment_link(int(get_order_total_price(order)), order.id)
        return Response(data={"payment_link": link})


@extend_schema(tags=["orderitems"])
class OrderitemsView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = OrderitemsModel.objects.all()
    serializer_class = ListOrderitemsSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListOrderitemsSerializer,
        "retrieve": RetrieveOrderitemsSerializer,
        "create": CreateOrderitemsSerializer,
    }


@extend_schema(tags=["basket"], summary="Konzinka")
class CartView(BaseViewSetMixin, ModelViewSet):
    serializer_class = ListCartSerializer
    permission_classes = [IsAuthenticated]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListCartSerializer,
        "retrieve": RetrieveCartSerializer,
        "create": CreateCartSerializer,
        "update": CreateCartSerializer,
        "partial_update": CreateCartSerializer,
    }

    def get_queryset(self):
        return CartModel.objects.order_by("-id").filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data.get("product")
        cart = CartModel.objects.filter(user=self.request.user, product_id=product)
        if cart.exists():
            cart.update(count=F("count") + 1)
            return
        serializer.save(user=self.request.user)
