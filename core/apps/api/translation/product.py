from modeltranslation.translator import TranslationOptions, register

from core.apps.api.models import CartModel, OrderitemsModel, OrderModel, ProductModel


@register(ProductModel)
class ProductTranslation(TranslationOptions):
    fields = []


@register(OrderModel)
class OrderTranslation(TranslationOptions):
    fields = []


@register(OrderitemsModel)
class OrderitemsTranslation(TranslationOptions):
    fields = []


@register(CartModel)
class CartTranslation(TranslationOptions):
    fields = []
