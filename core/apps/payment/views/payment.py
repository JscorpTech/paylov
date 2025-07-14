from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.apps.api.models import OrderModel
from core.apps.payment.serializers import PaylovCallbackSerializers
from core.apps.api.services.product import get_order_total_price
import logging
from core.apps.payment.exceptions import InvalidAmountException, OrderNotFoundException
from core.apps.api.enums.product import PaymentStatusEnum
from rest_framework import status
from core.apps.payment.models import TransactionModel
from core.apps.payment.enums import TransactionStatusEnum, PaymentProviderEnum
from drf_spectacular.utils import extend_schema
from core.apps.payment.services import uzs_to_usd, tiny_to_amount


@extend_schema(deprecated=True, tags=["payment"])
class PaymentViewset(GenericViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "paylov":
            return PaylovCallbackSerializers
        raise NotImplementedError(f"No serializer class defined for action: {self.action}")

    @action(methods=["POST"], detail=False, url_name="paylov", url_path="paylov")
    def paylov(self, request):
        try:
            serializer_class = self.get_serializer_class()
            ser = serializer_class(data=request.data)
            ser.is_valid(raise_exception=True)

            params = ser.validated_data.get("params")
            order_id = params.get("account", {}).get("order_id")
            amount = params.get("amount_tiyin")
            currency = int(params.get("currency", 860))

            order_qs = OrderModel.objects.filter(id=order_id)
            if not order_qs.exists():
                raise OrderNotFoundException("Order not found")

            order = order_qs.first()
            self.paylov_validate(order, amount, currency)

            method = ser.validated_data.get("method")
            logging.info(f"Paylov method: {method}")

            match method:
                case "transaction.check":
                    return self.paylov_check(request)
                case "transaction.perform":
                    return self.paylov_perform(order, amount, request, currency)
                case _:
                    return Response(
                        {
                            "jsonrpc": "2.0",
                            "id": request.data.get("id"),
                            "error": {"code": -32601, "message": "Method not found"},
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        except InvalidAmountException as e:
            logging.error(str(e))
            return self.response(request, 5, "invalid_amount")
        except OrderNotFoundException as e:
            logging.error(str(e))
            return self.response(request, 303, "order_not_found")

    def response(self, request, message="invalid_error", code=3):
        return Response(
            {
                "jsonrpc": "2.0",
                "id": request.data.get("id"),
                "result": {"status": code, "statusText": message},
            },
            status=status.HTTP_200_OK,
        )

    def paylov_perform(self, order, amount, request, currency):
        order.payment_status = PaymentStatusEnum.PAID.value
        order.save()
        TransactionModel.objects.create(
            amount=amount,
            currency=currency,
            order=order,
            status=TransactionStatusEnum.SUCCESS.value,
            provider=PaymentProviderEnum.PAYLOV.value,
        )
        return self.response(request, 0, "ok")

    def paylov_validate(self, order, amount, currency):
        expected_amount = get_order_total_price(order)
        if currency == 840:
            expected_amount = uzs_to_usd(expected_amount)
        if float(expected_amount) != tiny_to_amount(int(amount)):
            raise InvalidAmountException(
                "Invalid amount {} {} {} {}".format(
                    float(expected_amount), tiny_to_amount(int(amount)), currency, amount
                )
            )

    def paylov_check(self, request):
        return self.response(request, 0, "ok")
