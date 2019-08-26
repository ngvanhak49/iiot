from django.urls import path, include

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'entry', views.EntryViewSet)
router.register(r'thing', views.ThingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
