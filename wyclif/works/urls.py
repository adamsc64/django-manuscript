from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
	url(r'^$', views.all_works, name="all-titles"),
	url(r'^(?P<title>[-\w]+)/$', views.chapters, name="show-chapters"),
	url(r'^(?P<title>[-\w]+)/(?P<chapter>[-\w]+)/$', views.pages, name="show-pages"),
#	url(r'^(?P<title>.*)/(?P<model>.*)/?$', 				'model_by_work'),
#	url(r'^(?P<title>.*)/(?P<model>.*)/(?P<id>\d*)/?$', 	'element_by_id'),
)


