from django.conf.urls import include, url, patterns
from django.contrib import admin
from API import views, urls


urlpatterns = patterns('',
    url(r'^API/', include(urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index$', views.login_user, name='Login'),
    url(r'^logout$', views.logout_view, name='Logout'),
    url(r'^$', views.login_view, name='Login'),
)
