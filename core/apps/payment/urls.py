from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apps.payment.views import PaymentViewset

router = DefaultRouter()
router.register("", PaymentViewset, basename="payment")


urlpatterns = [
    path("", include(router.urls)),
]
