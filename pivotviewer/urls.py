from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^calcs', 'pivotviewer.views.RController'),
    url(r'^test', 'pivotviewer.views.current_datetime'),

)
