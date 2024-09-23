from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import LoanViewSet, PaymentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'loans', LoanViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
