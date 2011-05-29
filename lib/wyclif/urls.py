from django.conf.urls.defaults import *
from django.conf import settings
from django.http import HttpResponse

urlpatterns = patterns('')

urlpatterns += patterns('',
	(r'^/?$', 'wyclif.views.index'),
	(r'^input/?$', 'wyclif.views.input'),
)

urlpatterns += patterns('wyclif.work.views',
	(r'^work/?$', 											'all_works'),
	(r'^work/(?P<work>.*)/?$', 								'one_work'),
	(r'^work/(?P<work>.*)/(?P<model>.*)/?$', 				'model_by_work'),
	(r'^work/(?P<work>.*)/(?P<model>.*)/(?P<id>\d*)/?$', 	'element_by_id'),
)

urlpatterns += patterns('',
	(r'^sentry/', include('sentry.urls')),
)


#static media
urlpatterns += patterns('',
	(r'^static/(?P<path>.*)$',			'django.views.static.serve',
										{
											'document_root':	settings.STATIC_PATH,
											'show_indexes':		(settings.DEBUG==True)
										}
	),
	(r'^robots\.txt$', lambda response : HttpResponse("User-agent: *\r\nDisallow: /\r\n", mimetype="text/plain") ),
)

# implementing tastypie api.
from tastypie.api import Api
from wyclif.api import ParagraphResource, ChapterResource, TitleResource

v1_api = Api(api_name='v1')
v1_api.register(ParagraphResource())
v1_api.register(ChapterResource())
v1_api.register(TitleResource())

urlpatterns += patterns('',
	(r'^api/', include(v1_api.urls)),
)

from django.contrib import admin
admin.autodiscover()

urlpatterns += patterns('',
	(r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	(r'^accounts/login/', 				'django.contrib.auth.views.login', {'template_name': 'django/registration/login.html'}),
	(r'^accounts/logout/', 				'django.contrib.auth.views.logout', {'next_page': '/'})	,
)

# implementing /db/ views.

from wyclif.bin.csv_to_db import run_view
from wyclif.models import Paragraph, Title, Author

urlpatterns += patterns('',

	(r'^db/runimport/$', run_view),
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