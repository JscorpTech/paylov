from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TransactionStatusEnum(TextChoices):
    PENDING = "pending", _("pending")
    SUCCESS = (
        "success",
        _("success"),
    )
    CANCELED = "canceled", _("canceled")


class PaymentProviderEnum(TextChoices):
    PAYLOV = "paylov", _("paylov")
