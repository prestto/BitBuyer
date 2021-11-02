from articles.views import ArticleViewSet
from django.urls import path
# from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter

from coins.views import CoinViewSet

router = ExtendedSimpleRouter()
(
    router.register(r'', CoinViewSet, basename='coins')
          .register(
              r'articles',
              ArticleViewSet,
              basename='coins-articles',
              parents_query_lookups=['coins_abbreviation']
    )
)

urlpatterns = router.urls
