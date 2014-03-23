from django.conf.urls import patterns, include, url
from dashboard import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^summary/$', views.get_summary),
    url(r'^summary/(?P<scrip_id>\w+)/$', views.get_summary),
)
