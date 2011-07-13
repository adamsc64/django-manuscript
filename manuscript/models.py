import os

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.files.base import ContentFile

from datetime import datetime


class BaseModel(models.Model):
	class Meta:
		abstract = True

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in self._meta.fields]

	def get_admin_path(self):
		module_name = self._meta.module_name
		return reverse( 'admin:manuscript_%s_change' % module_name, args=(self.pk,) )
	
	def get_admin_link(self):
		path = self.get_admin_path()
		return "<a href='%s'>%s</a>" % (path,str(self))

	get_admin_link.allow_tags = True
	get_admin_link.short_description = 'Link'

	def get_children_links(self):
		for related in self._meta.get_all_related_objects():
			children = getattr(self,str(related.var_name)+"_set")
			links = []
			for child in children.all():
				links.append(child.get_admin_link())
			return "<br>".join(links)

	get_children_links.allow_tags = True
	get_children_links.short_description = 'Elements'

class Chapter(BaseModel):
	heading = models.CharField(max_length=50)
	title = models.ForeignKey("manuscript.Title", verbose_name="In Title")
	start_page_no = models.IntegerField()
	slug = models.SlugField(max_length=70, blank=True, verbose_name="Resource URL name")
	old_id = models.IntegerField(null=True, editable=False) # import field
	xml_chapter_id = models.CharField(max_length=10, null=True, editable=False) # import field
		
	def __unicode__(self):
		#return u"pk=%s, heading='%s'" % (self.pk,self.heading)
		return u"%s" % self.heading

	def save(self, *args, **kwargs):
		if not self.slug:  #execute only if there is not one already.
			slug = slugify( self.heading )
			# duplicates are ok.

			self.slug = slug

		super( Chapter, self ).save(*args, **kwargs)


class Page(BaseModel):
	title = models.ForeignKey("manuscript.Title", verbose_name="In Title")
	number = models.IntegerField(verbose_name="Page number")
	scan = models.ImageField(upload_to='pages', blank=True)
	
	def __unicode__(self):
		return u"p. %s" % unicode(self.number)
	
	class Meta:
		unique_together = ('title','number')
	
	def rename_scan_file(self, to):
		old_scan_name = self.scan.name
		if old_scan_name != to:
			self.scan.save("pages/"+to, ContentFile(self.scan.read()), save=True)
			os.remove(settings.MEDIA_ROOT + old_scan_name)
	
	def normalize_scan_filename(self):
		print "Normalizing page (%s)." % str(self)
		print "-- old scan.name=%s" % str(self.scan.name)

		to = "pages/" + str(self.title.slug) + "_p" + str(self.number) + ".jpg"
		self.rename_scan_file(to=to)

		print "-- new scan.name=%s" % str(self.scan.name)
		print
		
	def normalize_scan_image(self):
		#todo
		pass

	
def normalize_all_page_scan_filenames():
	for p in Page.objects.all():
		p.normalize_scan_filename()
		

class Paragraph(BaseModel):
	SPLIT_CHOICES = (
		("bottom", "This paragraph continues from page before"),
		("no", "Not split across pages"),
		("top", "This paragraph continues onto next page"),
	)
	
	chapter = models.ForeignKey('manuscript.Chapter', verbose_name="In Chapter")
	number = models.IntegerField(verbose_name="Order in Chapter")
	page = models.ForeignKey('manuscript.Page')
	split = models.CharField(max_length=10, choices=SPLIT_CHOICES)
	text = models.TextField()
	old_page_number = models.IntegerField(null=True, editable=False) # import field only
	old_id = models.IntegerField(null=True, editable=False) # import field only

	def __unicode__(self):
		return "Paragraph %s: %s" % (str(self.number),str(self.text[:100]))
		#return u"[%s] paragraph #%s in chapter, starting '%s...'" % (self.page, self.number, self.text[:20])
	
	def title(self):
		return self.page.title
			

class Title(BaseModel):
	text = models.CharField(verbose_name = "Title Text", max_length=70)
	author = models.ForeignKey("manuscript.Author")
	volume = models.IntegerField()
	pages = models.IntegerField()
	slug = models.SlugField(max_length=70, unique=True, blank=True, verbose_name="Resource URL name")

	old_id = models.IntegerField(null=True, editable=False) # import field

	def __unicode__(self):
		return u"%s" % self.text
	
	def save(self, *args, **kwargs):
		if not self.slug:  #execute only if there is not one already.
			slug = slugify( self.text )
			try:
				slug_double = Title.objects.get(slug__iexact = slug)
			except Title.DoesNotExist:
				#there is no slug by that title in the database.
				pass
			else:
				#there is a slug already by that title in the database.
				slug = slug + "-" + slugify(str(datetime.now()))

			self.slug = slug

		super( Title, self ).save(*args, **kwargs)


class Author(BaseModel):
	name = models.CharField(max_length=70)
	old_id = models.IntegerField(null=True, editable=False) # import field

	def __unicode__(self):
		return u"%s" % self.name

class SiteCopyText(models.Model):
	index = models.CharField(max_length=100)
	value = models.TextField(default="")
	
	def __unicode__(self):
		return self.value