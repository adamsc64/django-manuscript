# Copyright Christopher Adams, 2011
# All rights reserved.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'manuscript.views.all_works', name="all-works"),
	url(r'^(?P<title>[-\w]+)/$', 'manuscript.views.chapters', name="show-chapters"),
	url(r'^(?P<title>[-\w]+)/(?P<page>\d+)/$', 'manuscript.views.page', name="show-page"),
	url(r'^(?P<title>[-\w]+)/(?P<chapter>[-\w]+)/$', 'manuscript.views.chapter', name="show-chapter"),
#	url(r'^(?P<title>.*)/(?P<model>.*)/?$', 				'model_by_work'),
#	url(r'^(?P<title>.*)/(?P<model>.*)/(?P<id>\d*)/?$', 	'element_by_id'),
)


