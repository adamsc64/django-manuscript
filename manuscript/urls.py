# Copyright (C) 2011 by Christopher Adams
# Released under MIT License. See LICENSE.txt in the root of this
# distribution for details.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'manuscript.views.all_works', name="all-works"),
	url(r'^(?P<title>[-\w]+)/$', 'manuscript.views.whole_work', name="show-whole-work"),
	url(r'^(?P<title>[-\w]+)/list-chapters/$', 'manuscript.views.chapters', name="show-chapters"),
	url(r'^(?P<title>[-\w]+)/(?P<page>\d+)/$', 'manuscript.views.page', name="show-page"),
	url(r'^(?P<title>[-\w]+)/(?P<chapter>[-\w]+)/$', 'manuscript.views.chapter', name="show-chapter"),
#	url(r'^(?P<title>.*)/(?P<model>.*)/?$', 				'model_by_work'),
#	url(r'^(?P<title>.*)/(?P<model>.*)/(?P<id>\d*)/?$', 	'element_by_id'),

#   url(r'^img_to_db/run/$', 'wyclif.bin.img_to_db.run_view'),
#   url(r'^db/runimport/$', 'wyclif.bin.csv_to_db.run_view'),

)


