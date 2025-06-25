from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apps.api import views

router = DefaultRouter()
router.register("product", views.ProductView, basename="product")
router.register("order", views.OrderView, basename="order")
router.register("basket", views.CartView, basename="basket")

urlpatterns = [
    path("", include(router.urls)),
]
