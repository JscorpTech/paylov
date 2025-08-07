from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel

from core.apps.api.enums import OrderStatusEnum, PaymentStatusEnum


class ProductModel(AbstractBaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    price = models.FloatField(verbose_name=_("price"))
    quantity = models.IntegerField(verbose_name=_("quantity"))
    image = models.ImageField(verbose_name=_("image"),
                              upload_to="product",
                              default="product/default.png")
    description = models.TextField(verbose_name=_("description"),
                                   null=True,
                                   blank=True)

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
    user = models.ForeignKey(get_user_model(),
                             verbose_name="user",
                             related_name="orders",
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    is_notify = models.BooleanField(_("Is Notify"), default=False)
    payment_status = models.CharField(_("payment status"),
                                      choices=PaymentStatusEnum.choices,
                                      default=PaymentStatusEnum.PENDING)
    status = models.CharField(_("status"),
                              choices=OrderStatusEnum.choices,
                              default=OrderStatusEnum.CREATED,
                              max_length=20)

    # Order reciver info
    first_name = models.CharField(_("First Name"), null=True, blank=True)
    last_name = models.CharField(_("Last Name"), null=True, blank=True)
    phone = models.CharField(_("phone"), null=True, blank=True)
    company_name = models.CharField(_("Company Name"), null=True, blank=True)
    city = models.CharField(_("City"), null=True, blank=True)
    region = models.CharField(_("Region"), null=True, blank=True)
    district = models.CharField(_("District"), null=True, blank=True)
    comment = models.CharField(_("Comment"), null=True, blank=True)
    amount = models.BigIntegerField(_("amount"), null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._payment_status = self.payment_status

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _create_fake(self):
        return self.objects.create(user=get_user_model()._create_fake(), )

    class Meta:
        db_table = "order"
        verbose_name = _("OrderModel")
        verbose_name_plural = _("OrderModels")


class OrderitemsModel(AbstractBaseModel):
    order = models.ForeignKey(OrderModel,
                              verbose_name="order",
                              related_name="items",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,
                                verbose_name="product",
                                related_name="items",
                                on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name=_("count"), default=1)
    price = models.FloatField(verbose_name=_("price"))
    discount = models.FloatField(_("discount"), null=True, blank=True)

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


class CartModel(AbstractBaseModel):
    product = models.ForeignKey("ProductModel",
                                verbose_name=_("product"),
                                on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),
                             verbose_name=_("user"),
                             on_delete=models.CASCADE,
                             related_name="carts")
    count = models.PositiveIntegerField(_("count"), default=1)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _create_fake(self):
        return self.objects.create(name="mock", )

    class Meta:
        db_table = "cart"
        verbose_name = _("CartModel")
        verbose_name_plural = _("CartModels")
