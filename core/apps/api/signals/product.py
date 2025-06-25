from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.api.models import CartModel, OrderitemsModel, OrderModel, ProductModel
from core.apps.api.enums import PaymentStatusEnum
from core.apps.api.services import subtrackt_product_quantity_from_order, add_product_quantity_from_order


@receiver(post_save, sender=ProductModel)
def ProductSignal(sender, instance, created, **kwargs): ...


@receiver(post_save, sender=OrderModel)
def OrderSignal(sender, instance, created, **kwargs):
    if instance._payment_status != instance.payment_status:
        if instance.payment_status == PaymentStatusEnum.PAID.value:
            subtrackt_product_quantity_from_order(instance)
        elif (
            instance._payment_status == PaymentStatusEnum.PAID.value
            and instance.payment_status != PaymentStatusEnum.PAID.value
        ):
            add_product_quantity_from_order(instance)


@receiver(post_save, sender=OrderitemsModel)
def OrderitemsSignal(sender, instance, created, **kwargs): ...


@receiver(post_save, sender=CartModel)
def CartSignal(sender, instance, created, **kwargs): ...
