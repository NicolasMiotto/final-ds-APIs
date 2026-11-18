from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanetaViewSet

router = DefaultRouter()
router.register(r'planetas', PlanetaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]