"""Module to get images from old wyclif project, from web, into new model. Use run() at commandline or run_view() in urls.py."""

import urllib2
import os

from django.conf import settings
from django.http import HttpResponse
from django.core.files import File

import sgmllib

from wyclif.models import Page

class HTMLJPGParser(sgmllib.SGMLParser):
	"""To parse HTML to find links to JPG files."""
	
	def parse(self, str):
		self.feed(str)
		self.close()

	def __init__(self, verbose=0):
		sgmllib.SGMLParser.__init__(self, verbose)  #super.
		self.jpg_hyperlinks = []
	
	def start_a(self, attributes):
		"""Process an <a> for a jpg."""
		
		for name, value in attributes:
			if name == "href":
				if ".jpg" in value.lower() or ".jpeg" in value.lower():
					self.jpg_hyperlinks.append(value)
	
	def get_jpg_hyperlinks(self):
		return self.jpg_hyperlinks
	


def run(run_silently=True): # "/Users/chris/coding/wyclif_project/wyclif/lib/wyclif/bin/"
	"""Downloads all the old wyclif images into MEDIA/temp directory."""

	if not run_silently:
		print "Going to download all old wyclif image files."

	try:
		os.mkdir(settings.MEDIA_ROOT+"temp")
	except OSError:
		#directory already exists.
		pass
		
	for page in Page.objects.all():
		if not run_silently:
			print "Running title.old_id=%s, page.number=%s." % (page.title.old_id, page.number)

		htmlresponse = urllib2.urlopen("http://www9.georgetown.edu/faculty/szittyap/wyclif/index.cfm?action=dsp_volume&titleID=%s&pageNo=%s" % (str(page.title.old_id) , str(page.number)))
		html = htmlresponse.read()
	
		parser = HTMLJPGParser()
		parser.parse(html)
	
		jpg_urls = parser.get_jpg_hyperlinks()
	
		for jpg_url in jpg_urls:

			try:
				jpgresponse = urllib2.urlopen(jpg_url)
			except urllib2.HTTPError, e:
				if not run_silently:
					print "Ignored HTTPError at %s." % jpg_url
			else:
				jpg = jpgresponse.read()

				path = settings.MEDIA_ROOT +"temp/"
				filename = "title_old_id_%02d__page_number_%04d.jpg" % (page.title.old_id, page.number)
				dest = path + filename

				#write temporary file.
				file_object = File(open(dest, "w"))
				file_object.write(jpg)
				file_object.close()

				#read temporary file
				file_object = File(open(dest, "r"))
				page.scan.save(filename, file_object)				
				file_object.close()
				
				#delete temporary file
				os.remove(dest)

				if not run_silently:
					print "Saved %s from %s." % (dest,jpg_url)

			#page.scan = 

	if not run_silently:
		print "Done with run."
	
	return


def run_view(request):
	"""A wrapper view to be used in urls.py for the run() function."""
	run(run_silently=True)
	return HttpResponse("The import seems to have run without failing! %s" % (time.ctime()))

