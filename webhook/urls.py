from django.urls import path, include
from rest_framework import routers
from webhook.views import UserViewSet, PostsViewSet, AcessosViewSet, AcessosPorPeriodoViewSet, UTMViewSet, WebhookViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='Users')
router.register('posts', PostsViewSet, basename='Pots')
router.register('acessos', AcessosViewSet, basename='Acessos')
router.register('utms', UTMViewSet, basename='UTMs')

urlpatterns = [
    path('', include(router.urls)),
    path('acessos/<str:dataInicial>/<str:dataFinal>/data/', AcessosPorPeriodoViewSet.as_view()),
    path('webhook/', WebhookViewSet.as_view())
]