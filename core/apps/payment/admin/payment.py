from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from core.apps.payment.models import TransactionModel
from core.apps.payment.enums import TransactionStatusEnum


@admin.register(TransactionModel)
class TransactionAdmin(ModelAdmin):
    list_display = (
        "id",
        "amount",
        "order__id",
        "currency",
        "_status",
        "_provider",
    )

    @display(description="provider", label=True)
    def _provider(self, obj):
        return obj.provider

    @display(
        description="status",
        label={
            TransactionStatusEnum.CANCELED.value: "danger",
            TransactionStatusEnum.PENDING: "waring",
            TransactionStatusEnum.SUCCESS.value: "success",
        },
    )
    def _status(self, obj):
        return obj.status
