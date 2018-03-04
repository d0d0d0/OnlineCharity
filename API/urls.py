from django.conf.urls import url, patterns
from API.views import repr_list, repr_indv, logout_view

urlpatterns = patterns(
    'API.views',
    url(r'^(?P<typ>[A-Za-z]+)/$', repr_list),
    url(r'^(?P<typ>[A-Za-z]+)/(?P<tc_no>[0-9]{11})$', repr_indv),
    url(r'^(?P<typ>[A-Za-z]+)/(?P<name>[A-Za-z]+)$', repr_indv),
)
