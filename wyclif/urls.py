# Copyright Christopher Adams, 2011
# All rights reserved.

from django.conf.urls.defaults import *
from django.conf import settings
from django.http import HttpResponse

urlpatterns = patterns('')

urlpatterns += patterns('',
	(r'^/?$', 'wyclif.views.index'),

	# site
	(r'^works/', include('wyclif.works.urls')),
	(r'^about/+$', 'wyclif.views.about'),
	(r'^copyright/+$', 'wyclif.views.copyright'),
	(r'^search/+$', 'wyclif.views.search'),
	(r'^contact/+$', 'wyclif.views.contact'),
)

#static media
urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$',			'django.views.static.serve',
										{
											'document_root':	settings.MEDIA_ROOT,
											'show_indexes':		(settings.DEBUG==True)
										}
	),
	(r'^static/(?P<path>.*)$',			'django.views.static.serve',
										{
											'document_root':	settings.STATIC_ROOT,
											'show_indexes':		(settings.DEBUG==True)
										}
	),
	(r'^robots\.txt$', lambda response : HttpResponse("User-agent: *\r\nDisallow: /\r\n", mimetype="text/plain") ),
)

from django.contrib import admin
admin.autodiscover()

urlpatterns += patterns('',
	(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# data input tool.
	(r'^input/?$', 'wyclif.views.input'),
	
	# django-sentry for debugging.
	(r'^sentry/', include('sentry.web.urls')),

	(r'^favicon\.ico$', 'wyclif.views.favicon'),

)


# implementing /db/ views.

from manuscript.models import Paragraph, Title, Author

urlpatterns += patterns('',

	#(r'^img_to_db/run/$', 'wyclif.bin.img_to_db.run_view'),

	#(r'^db/runimport/$', 'wyclif.bin.csv_to_db.run_view'),
	(r'^db/paragraphs/$', 'django.views.generic.list_detail.object_list', {
		'queryset' : Paragraph.objects.all(),
		'template_name' : 'wyclif/object_list.html'
	}),
#		'extra_context' : { 'fieldnames' : Paragraph._meta.get_all_field_names() }
	(r'^db/titles/$', 'django.views.generic.list_detail.object_list', {
		'queryset' : Title.objects.all(),
		'template_name' : 'wyclif/object_list.html'
	}),
	(r'^db/authors/$', 'django.views.generic.list_detail.object_list', {
		'queryset' : Author.objects.all(),
		'template_name' : 'wyclif/object_list.html'
	}),

)

handler500 = 'wyclif.views.error_view'
