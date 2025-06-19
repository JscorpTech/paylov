from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.api.models import OrderitemsModel, OrderModel, ProductModel


@receiver(post_save, sender=ProductModel)
def ProductSignal(sender, instance, created, **kwargs): ...


@receiver(post_save, sender=OrderModel)
def OrderSignal(sender, instance, created, **kwargs): ...


@receiver(post_save, sender=OrderitemsModel)
def OrderitemsSignal(sender, instance, created, **kwargs): ...
