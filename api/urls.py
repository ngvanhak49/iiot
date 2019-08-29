from django.urls import path, include, re_path

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'entry', views.EntryViewSet)
router.register(r'thing', views.ThingViewSet)
router.register(r'thingdata', views.ThingDataViewSet)
router.register(r'company', views.CompanyViewSet)
router.register(r'department', views.DeparmentViewSet)
#router.register(r'rulereport', views.ThingRuleReportViewSet)
router.register(r'ruleengine', views.RuleEngineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path(r'^rulereport/(?P<thing>[\w\-]+)/$', views.ThingRuleReportViewSet.as_view()),
    re_path(r'^rulereport/$', views.ThingRuleReportViewSet.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
