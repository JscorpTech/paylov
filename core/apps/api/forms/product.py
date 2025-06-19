from django import forms

from core.apps.api.models import OrderitemsModel, OrderModel, ProductModel


class ProductForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = "__all__"


class OrderForm(forms.ModelForm):

    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderitemsForm(forms.ModelForm):

    class Meta:
        model = OrderitemsModel
        fields = "__all__"
