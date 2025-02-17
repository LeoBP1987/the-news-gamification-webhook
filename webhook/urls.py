from django.urls import path, include
from rest_framework import routers
from webhook.views import UserViewSet, PostsViewSet, AcessosViewSet, AcessosPorPeriodoViewSet, UTMViewSet, WebhookViewSet
from oauth2_provider import urls as oauth2_urls

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='Users')
router.register('posts', PostsViewSet, basename='Posts')
router.register('acessos', AcessosViewSet, basename='Acessos')
router.register('utms', UTMViewSet, basename='UTMs')

urlpatterns = [
    path('', include(router.urls)),
    path('acessos/<str:dataInicial>/<str:dataFinal>/data/', AcessosPorPeriodoViewSet.as_view(), name='Acessos-Por-Periodo'),
    path('webhook/', WebhookViewSet.as_view(), name='Webhook'),
    path('oauth2/', include(oauth2_urls))
]