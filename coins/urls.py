from django.urls import path
from rest_framework.routers import DefaultRouter
from coins.views import CoinViewSet


router = DefaultRouter()
router.register(r'', CoinViewSet)
urlpatterns = router.urls
