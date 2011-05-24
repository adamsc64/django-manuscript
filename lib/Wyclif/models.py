from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#class Profile(models.Model):
#	# This field connects each profile with a user.
#    user = models.OneToOneField(User)
#
#	# Any number of other fields can go below.
#	# ...
#
##create a profile automatically whenever a User is created.
#def create_profile(sender, **kw):
#    user = kw["instance"]
#    if kw["created"]:
#        profile = Profile()
#        profile.user = user
#       	profile.save()
#post_save.connect(create_profile, sender=User)


class wyclifModel(models.Model):
	class Meta:
		abstract = True

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in self._meta.fields]


class Chapter(wyclifModel):
	heading = models.CharField(max_length=50)
	title = models.ForeignKey("wyclif.Title", verbose_name="In Title")
	start_page_no = models.IntegerField()
	old_id = models.IntegerField(null=True, editable=False) # import field
	xml_chapter_id = models.CharField(max_length=10, null=True, editable=False) # import field
	
	def __unicode__(self):
		#return u"pk=%s, heading='%s'" % (self.pk,self.heading)
		return u"(%s) '%s'" % (self.title , self.heading)


class Page(wyclifModel):
	title = models.ForeignKey("wyclif.Title", verbose_name="In Title")
	number = models.IntegerField(verbose_name="Page number")
	scan = models.ImageField(upload_to='pages')
	
	def __unicode__(self):
		return u"%s, p. %s" % (unicode(self.title), unicode(self.number))
	
	class Meta:
		unique_together = ('title','number')
		

class Paragraph(wyclifModel):
	SPLIT_CHOICES = (
		("bottom", "Bottom of page to top of next page"),
		("no", "Not split across pages"),
		("top", "Top of page from bottom of last page"),
	)
	
	chapter = models.ForeignKey('wyclif.Chapter', verbose_name="In Chapter")
	number = models.IntegerField(verbose_name="Order in Chapter")
	page = models.ForeignKey('wyclif.Page')
	split = models.CharField(max_length=10, choices=SPLIT_CHOICES)
	text = models.TextField()
	old_page_number = models.IntegerField(null=True, editable=False) # import field only
	old_id = models.IntegerField(null=True, editable=False) # import field only

	def __unicode__(self):
		return u"[%s] '%s...'" % (self.pk,self.text[:20])
	

class Title(wyclifModel):
	text = models.CharField(verbose_name = "Title Text", max_length=70)
	author = models.ForeignKey("wyclif.Author")
	volume = models.IntegerField()
	pages = models.IntegerField()
	old_id = models.IntegerField(null=True, editable=False) # import field

	def __unicode__(self):
		return u"%s" % self.text

	
class Author(wyclifModel):
	name = models.CharField(max_length=70)
	old_id = models.IntegerField(null=True, editable=False) # import field

	def __unicode__(self):
		return u"%s" % self.name

