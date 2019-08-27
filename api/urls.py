from django.urls import path, include

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'entry', views.EntryViewSet)
router.register(r'thing', views.ThingViewSet)
router.register(r'thingdata', views.ThingDataViewSet)
router.register(r'company', views.CompanyViewSet)
router.register(r'department', views.DeparmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
