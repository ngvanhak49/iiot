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
router.register(r'customer', views.CustomerViewSet)
router.register(r'organization', views.OrganizationViewSet)
#router.register(r'organizationid', views.OrganizationByIDViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path(r'^rulereport/(?P<thing>[\w\-]+)/$', views.ThingRuleReportViewSet.as_view()),
    re_path(r'^rulereport/$', views.ThingRuleReportViewSet.as_view()),
    re_path(r'^v1/customer/$', views.v1_CustomerViewSet.as_view()),
    re_path(r'^v1/company/$', views.v1_CompanyViewSet.as_view()),
    #re_path(r'^v1/organization/$', views.v1_OrganizationViewSet.as_view()),
    re_path(r'^v1/organizationbyid/$', views.v1_OrganizationByIDViewSet.as_view()),
    re_path(r'^v1/entrybyowner/$', views.v1_EntryByOwnerViewSet.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
