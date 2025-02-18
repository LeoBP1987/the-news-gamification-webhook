from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from webhook.views import WebhookViewSet
from django.views.generic import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="The News Gamification API",
      default_version='v1',
      description="API para o aplicativo de gamificação do site The News",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="leonardobp1987@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('', WebhookViewSet.as_view(), name='Webhook-Raiz'),
    path('admin/', admin.site.urls),
    path('', include('webhook.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
