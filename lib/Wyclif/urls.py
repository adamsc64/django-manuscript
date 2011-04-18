from django.conf.urls.defaults import *
from django.conf import settings
from django.http import HttpResponse

from django.contrib import admin
admin.autodiscover()

from views import index

# implementing tastypie api.
from tastypie.api import Api
#from Nexus.outwardapi import TransactionResource, UserResource

v1_api = Api(api_name='v1')
#v1_api.register(TransactionResource())


urlpatterns = patterns('',
	(r'^/?$', index),
	
	(r'api/', include(v1_api.urls)),
    (r'^sentry/', include('sentry.urls')),
#	(r'^googled05e050f361f6ab1\.html$', 'Nexus.views.googleproof'),
	(r'^robots\.txt$', 'robotstxt'),
	(r'^static/(?P<path>.*)$',			'django.views.static.serve',
										{
											'document_root':	settings.STATIC_PATH,
											'show_indexes':		True
										}
	),

#	(r'^media/(?P<path>.*)$',			'django.views.static.serve',
#										{
#											'document_root':	settings.ADMIN_MEDIA_LOC,
#											'show_indexes':		True
#										}
#	),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
   	(r'^admin/',						include(admin.site.urls)),

	(r'^accounts/login/', 				'django.contrib.auth.views.login', {'template_name': 'django/registration/login.html'}),
	(r'^accounts/logout/', 				'django.contrib.auth.views.logout', {'next_page': '/'})	,
)

if settings.DEBUG==False:
	urlpatterns += patterns('',
	   	(r'^.*$',						'Nexus.views.do404',)
	)
