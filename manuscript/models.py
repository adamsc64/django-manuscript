# Copyright Christopher Adams, 2011
# All rights reserved.

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files import File

from datetime import datetime
import PIL

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
		return u"%s: %s" % (self.title.text , self.heading)

	def save(self, *args, **kwargs):
		if not self.slug:  #execute only if there is not one already.
			slug = slugify( self.heading )
			# duplicates are ok.

			self.slug = slug

		super( Chapter, self ).save(*args, **kwargs)
	
	@models.permalink
	def get_absolute_url(self):
		return ('show-chapter', (), {
			'chapter': self.slug,
			'title': self.title.slug,
		})	
	
	def get_full_paragraphs(self):
		#paragraphs = self.paragraph_set.all().order_by('number')

		paragraphs = Paragraph.objects.filter(chapter=self)
		numbers = list(set(paragraphs.values_list('number',flat=True)))
		full_paragraphs = [get_logical_paragraph_text(chapter=self, paragraph_number=number) for number in numbers]

		return full_paragraphs

	def get_first_paragraph(self):
		paragraphs = self.paragraph_set.all()

		if not paragraphs:
			raise Paragraph.DoesNotExist

		first_number = list(set(paragraphs.values_list('number', flat=True)))[0]
		paragraphs = paragraphs.filter(number=first_number)
		pages = paragraphs.values_list('page', flat=True).order_by('number')
		first_page = pages[0]

		first_paragraph = None

		for split in Paragraph.SPLIT_PRIORITY:
			try:
				first_paragraph = paragraphs.get(page=first_page, split=split)
			except Paragraph.DoesNotExist:
				pass
			else:
				break

		if not first_paragraph:
			raise Paragraph.DoesNotExist
		else:
			return first_paragraph

	def get_first_page(self):
		first_paragraph = self.get_first_paragraph()
		return first_paragraph.page

	def next(self):
		"""
		Returns the next chapter in this chapter's title. If this is the last
		chapter, returns None.
		"""

		next_chapters_in_title = Chapter.objects.filter(
			title = self.title,
			start_page_no__gt = self.start_page_no,
		).order_by('start_page_no')

		if next_chapters_in_title.count() > 0:
			return next_chapters_in_title[0]
		else:
			return None



def get_logical_paragraph_elements(chapter, paragraph_number):
	elements = Paragraph.objects.filter(chapter=chapter, number=paragraph_number)
	if elements.count() < 1:
		raise Paragraph.DoesNotExist

	l = []
	for step in Paragraph.SPLIT_PRIORITY:
		elements_in_paragraph = elements.filter(split=step).order_by('page__number')
		if elements_in_paragraph.count() > 0:
			for el in elements_in_paragraph:
				l.append(el)
	return l


def get_logical_paragraph_text(chapter, paragraph_number):
	elements = get_logical_paragraph_elements(chapter, paragraph_number)

	result_text = ""

	for el in elements:
		result_text = result_text.strip() + " " + (el.text).strip()

	return result_text.strip()


class Page(BaseModel):
	title = models.ForeignKey("manuscript.Title", verbose_name="In Title")
	number = models.IntegerField(verbose_name="Page number")
	scan = models.ImageField(upload_to='original_scans', blank=True) # original scan
	display = models.ImageField(upload_to='pages_to_display', blank=True, verbose_name='display preview') # for site
	
	class Meta:
		unique_together = ('title','number')
	
	def next(self):
		try:
			return Page.objects.get(
				title = self.title,
				number = self.number+1,
			)
		except Page.DoesNotExist:
			return None
	
	def __unicode__(self):
		return u"%s, p. %s" % (unicode(self.title.text), unicode(self.number))
	
	def save(self, *args, **kwargs):
		# Call super.
		super( Page, self ).save(*args, **kwargs)

		# Process generation of resized image for site display.
		if hasattr(self.scan,"path"): # If scan exists.
			if not hasattr(self.display,"path"): # But display doesn't.
				#self.convert_scan_to_display() # avoids infinite loop.
				pass # do nothing for now until we figure out jpeg decoder on server.
	
	
	#def rename_scan_file(self, to):
	#	old_scan_name = self.scan.name
	#	if old_scan_name != to:
	#		self.scan.save("pages/"+to, ContentFile(self.scan.read()), save=True)
	#		os.remove(settings.MEDIA_ROOT + old_scan_name)

	#def normalize_scan_filename(self):
	#	print "Normalizing page (%s)." % str(self)
	#	print "-- old scan.name=%s" % str(self.scan.name)
    #
	#	to = "pages/" + self.get_normalized_filename()
	#	self.rename_scan_file(to=to)
    #
	#	print "-- new scan.name=%s" % str(self.scan.name)
	#	print
	
	def get_normalized_jpg_filename(self):
		return str(self.title.slug) + "_p" + str(self.number) + ".jpg"
	
	def convert_scan_to_display(self, commit=True):
		if hasattr(self.scan,"path"): # If scan exists.
			if not hasattr(self.display,"path"): # But display doesn't.
				(width , height) = (self.scan.width , self.scan.height)
		
				target_width = settings.MANUSCRIPT_DEFAULT_WIDTH
				target_height = int(1.0 * target_width / width * height)
				target_size = (target_width , target_height)
				target_path = settings.MEDIA_ROOT + "pages_to_display/" + self.get_normalized_jpg_filename()
		
				print "%s: Converting %s %s file to %s %s (new file)." % (str(self), str(self.scan.path), str((width,height)), str(target_path), str(target_size))
				PIL.Image.open(self.scan.path).resize(target_size).save(target_path)
		
				self.display = "pages_to_display/" + self.get_normalized_jpg_filename()
				if commit:
					self.save()
	

class Paragraph(BaseModel):
	SPLIT_CHOICES = (
		("bottom", "This paragraph continues from page before"),
		("no", "Not split across pages"),
		("top", "This paragraph continues onto next page"),
		("both", "This paragraph continues from last page AND goes to next page"),
	)
	SPLIT_PRIORITY = ("no","top","both","bottom")
	
	chapter = models.ForeignKey('manuscript.Chapter', verbose_name="in chapter")
	number = models.IntegerField(verbose_name="order in chapter")
	page = models.ForeignKey('manuscript.Page', verbose_name="on page")
	split = models.CharField(max_length=10, choices=SPLIT_CHOICES, verbose_name="split across pages")
	text = models.TextField()
	old_page_number = models.IntegerField(null=True, editable=False) # import field only
	old_id = models.IntegerField(null=True, editable=False) # import field only

	composite = models.ForeignKey('manuscript.CompositeParagraph', null=True, blank=True, editable=False, verbose_name="composite")

	class Meta:
		order_with_respect_to = 'chapter'  #page?
		ordering = ('chapter','number',)

		#chapter.set_paragraph_order([1,2,3])
		#chapter.get_paragraph_order()
		#
		#paragraph = get()
		#next = paragraph.get_next_in_order()
		#prev = paragraph.get_previous_in_order()

	def __unicode__(self):
		return u"Paragraph %s: %s" % (unicode(self.number),unicode(self.text[:100]))
		#return u"[%s] paragraph #%s in chapter, starting '%s...'" % (self.page, self.number, self.text[:20])
	
	def title(self):
		return self.page.title
	
	def next(self):
		next_paragraph = None

		raise Exception("needs more testing")

		# First, try the next paragraph in this paragraph number and page by
		# split priority.
		i = Paragraph.SPLIT_PRIORITY.index(str(self.split)) + 1
		while i < len(Paragraph.SPLIT_PRIORITY) and not next_paragraph:
			next_group = Paragraph.objects.filter(
				chapter = self.chapter,
				number = self.number,
				page = self.page,
				split = Paragraph.SPLIT_PRIORITY[i]
			)
			if next_group.count() > 0:
				next_paragraph = next_group[0]

			i = i + 1
		
		if not next_paragraph:
			for split in Paragraph.SPLIT_PRIORITY:
				next_group = Paragraph.objects.filter(
					chapter = self.chapter,
					number = self.number,
					page = self.page.next(),
					split = split,
				)
				if next_group.count() > 0:
					next_paragraph = next_group[0]
				else:
					break
		
		if not next_paragraph:
			next_number_group = Paragraph.objects.filter(
				chapter = self.chapter,
				number = self.number+1,
			)
			for split in Paragraph.SPLIT_PRIORITY:
				try:
					next_paragraph = next_number_group.get(split=split)
				except Paragraph.DoesNotExist:
					pass
				else:
					break
		
		if not next_paragraph:
			next_chapter = self.chapter.next()
			if next_chapter:
				next_paragraph = next_chapter.get_first_paragraph()

		return next_paragraph
			
	def _follow_and_print(self):
		pi = self
		while pi:
			print pi.chapter, pi.number
			pi = pi.next()

def printif(istrue, text):
	if istrue:
		print text

def reset_paragraph_order(verbose=False):

	for chapter in Chapter.objects.all():
		printif(verbose, chapter)

		paragraphs = chapter.paragraph_set.all()
		numbers = list(set(paragraphs.values_list('number',flat=True)))

		sorted_ids = []

		for number in numbers:
#			printif(verbose, number)
			elements = paragraphs.filter(number=number)

#			printif(verbose, "Calculating: ")

			PRIORITY = ("no","top","both","bottom")

			for step in PRIORITY:
#				printif(verbose, step)
				
				found = elements.filter(split=step).order_by('page__number')
				for element in found:
#					printif(verbose, "   %s: %s" % (str(element.pk), element.text[:40]))
					sorted_ids.append(element.id)

		printif(verbose, sorted_ids)
		chapter.set_paragraph_order(sorted_ids)

	printif(verbose,"Finished.")
	
class CompositeParagraph(BaseModel):
	
	chapter = models.ForeignKey('manuscript.Chapter', verbose_name="in chapter")
	number = models.IntegerField(verbose_name="order in chapter")
	pages = models.ManyToManyField('manuscript.Page', verbose_name="on pages")
	text = models.TextField()

	def __unicode__(self):
		return u"CompositeParagraph %s: %s" % (unicode(self.number),unicode(self.text[:100]))
	
	def title(self):
		return self.page.title

def compile_paragraphs(flush=False, verbose=True):
	if flush:
		while CompositeParagraph.objects.all().count() > 0:
			# SQLite does not delete groups well ("DatabaseError: too many SQL variables")
			# so do it in chunks.
			for chapter in Chapter.objects.all():
				CompositeParagraph.objects.filter(chapter=chapter).delete()

	for chapter in Chapter.objects.all():

		paragraphs = Paragraph.objects.filter(chapter=chapter, composite__isnull=True)
		numbers = list(set(paragraphs.values_list('number',flat=True)))
	
		for number in numbers:
			elements = paragraphs.filter(chapter=chapter, number=number)
			if verbose:
				print "Combining: "
				for element in elements:
					print "   %s: %s" % (element.pk, element.text[:40])


			PRIORITY = ("no","top","both","bottom")
			
			result_text = ""
			
			for step in PRIORITY:
				elements_in_paragraph = elements.filter(split=step).order_by('page__number')
				texts = elements_in_paragraph.values_list('text',flat=True)
				for text in texts:
					result_text = result_text.strip() + " " + text.strip()
					
			pages = elements.values_list('page__pk', flat=True)
			pages = Page.objects.filter(pk__in=pages)
			
			new_composite = CompositeParagraph(
				chapter = chapter,
				number = number,
				text = result_text,
			)
			new_composite.save()
			for page in pages:
				new_composite.pages.add(page)
			new_composite.save()
			
			#Save foreignkey relation on paragraphs.
			for element in elements:
				element.composite = new_composite
				element.save()
			
			if verbose:
				print "Created:\n   %s" % str(new_composite.text)
				print "---"
			
	if verbose:
		print "Finished."
		

class Title(BaseModel):
	text = models.CharField(verbose_name="title text", max_length=70)
	author = models.ForeignKey("manuscript.Author")
	volume = models.IntegerField(verbose_name='volume number')
	publication_year = models.CharField(max_length=15, blank=True)
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


class SiteCopyTextManager(models.Manager):
	def get_or_create_for(self, index):
		copy_text, created = self.get_or_create(
			index=index,
			defaults={'value' : "Text for %s" % index}
		)
		return copy_text, created
		

class SiteCopyText(models.Model):
	index = models.CharField(max_length=100)
	value = models.TextField(default="")
	
	objects = SiteCopyTextManager()
	
	def __unicode__(self):
		return self.value
