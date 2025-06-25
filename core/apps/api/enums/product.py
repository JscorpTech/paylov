from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class PaymentStatusEnum(TextChoices):
    PENDING = "pending", _("pending")
    PAID = "paid", _("paid")
    CANCELED = "canceled", _("canceled")


class OrderStatusEnum(TextChoices):
    CREATED = "created", _("created")
    DELIVERED = "delivered", _("delivered")
    CANCELED = "canceled", _("canceled")