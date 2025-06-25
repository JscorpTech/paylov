from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from core.apps.payment.enums import TransactionStatusEnum, PaymentProviderEnum
from core.apps.api.models import OrderModel


class TransactionModel(AbstractBaseModel):
    amount = models.BigIntegerField(verbose_name=_("amount"))
    currency = models.PositiveIntegerField(_("currency"), default=860)
    order = models.ForeignKey("api.OrderModel", verbose_name=_("order"), on_delete=models.CASCADE)
    status = models.CharField(
        _("status"), max_length=20, choices=TransactionStatusEnum.choices, default=TransactionStatusEnum.PENDING
    )
    provider = models.CharField(_("payment provider"), choices=PaymentProviderEnum.choices)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            amount=10000,
            currency=860,
            order=OrderModel._fake_create(),
            status=TransactionStatusEnum.SUCCESS,
            property=PaymentProviderEnum.PAYLOV,
        )

    class Meta:
        db_table = "paylovTransaction"
        verbose_name = _("PaylovtransactionModel")
        verbose_name_plural = _("PaylovtransactionModels")
