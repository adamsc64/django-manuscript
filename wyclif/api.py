from tastypie.resources import ModelResource
from tastypie import fields

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL

from django.contrib.auth.models import User
#from wyclif.models import Profile
from wyclif.models import Chapter, Paragraph, Title

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'

		list_allowed_methods = ['get']
		
		authentication = Authentication()
		
		excludes = [
			"email",
			"password",
			"is_superuser",
			"first_name",
			"last_name",
			"date_joined",
			"last_login",
			"is_staff",
			"username",
			"is_active"
		]

#class ProfileResource(ModelResource):
#	class Meta:
#		queryset = Profile.objects.all()
#		resource_name = 'profile'
#
#		list_allowed_methods = ['get']
#
#		authentication = Authentication()

class ChapterResource(ModelResource):
	class Meta:
		queryset = Chapter.objects.all()
		resource_name = "chapter"
		list_allowed_methods = ['get','post']

		authentication = Authentication()
		authorization = Authorization()


class ParagraphResource(ModelResource):

	class Meta:
		queryset = Paragraph.objects.all()
		resource_name = "paragraph"
		list_allowed_methods = ['get','post']

		authentication = Authentication()
		authorization = Authorization()

class TitleResource(ModelResource):

	class Meta:
		queryset = Title.objects.all()
		resource_name = "title"
		list_allowed_methods = ['get','post']

		authentication = Authentication()
		authorization = Authorization()

