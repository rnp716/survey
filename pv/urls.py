from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from django.contrib import admin
from django.conf import settings
admin.autodiscover()

def index(request):
	return redirect('./index.html')

urlpatterns = patterns('',
    url(r'^project_list.json', 'pv.project_list.ProjectList'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', 'pv.urls.index'), # matches '' and '/'	
    url(r'^(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': settings.STATIC_URL, 'show_indexes' : True}),

)
