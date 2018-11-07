from django.conf.urls import include, patterns, url
from tastypie.api import Api

urlpatterns_getoverviewmaps = patterns(
    'climate.views',
    url(r'^climateinfo$', 'getClimateVillage', name='getClimateVillage'),   
)

urlpatterns = [
    url(r'^getOverviewMaps/', include(urlpatterns_getoverviewmaps)),
]
