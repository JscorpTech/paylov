from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from django.contrib.auth import get_user_model


class ProductModel(AbstractBaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    price = models.FloatField(verbose_name=_("price"))
    quantity = models.IntegerField(verbose_name=_("quantity"))
    image = models.ImageField(verbose_name=_("image"), upload_to="product", default="product/default.png")
    description = models.TextField(verbose_name=_("description"), null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="mock",
            price=1.0,
            quantity=1,
            description="mock",
        )

    class Meta:
        db_table = "product"
        verbose_name = _("ProductModel")
        verbose_name_plural = _("ProductModels")


class OrderModel(AbstractBaseModel):
    user = models.ForeignKey(get_user_model(), verbose_name="user", related_name="orders", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            user=get_user_model()._create_fake(),
        )

    class Meta:
        db_table = "order"
        verbose_name = _("OrderModel")
        verbose_name_plural = _("OrderModels")


class OrderitemsModel(AbstractBaseModel):
    order = models.ForeignKey(OrderModel, verbose_name="order", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, verbose_name="product", related_name="items", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_("quantity"))
    price = models.FloatField(verbose_name=_("price"))

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            order=OrderModel._create_fake(),
            product=ProductModel._create_fake(),
            price=1.0,
            quantity=1,
        )

    class Meta:
        db_table = "orderitems"
        verbose_name = _("OrderitemsModel")
        verbose_name_plural = _("OrderitemsModels")
