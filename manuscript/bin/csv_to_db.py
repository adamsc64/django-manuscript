# Copyright (C) 2011 by Christopher Adams
# Released under MIT License. See LICENSE.txt in the root of this
# distribution for details.

"""Module to import sample csv data into model. Use run() at commandline or run_view() in urls.py."""

import csv
import os
import time

from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse

from manuscript.models import Chapter, Paragraph, Title, Author, Page


def run(PATH_TO_FILES = os.path.dirname(os.path.abspath(__file__)) + os.sep, run_silently=True): # "/Users/chris/coding/wyclif_project/wyclif/lib/wyclif/bin/"
	"""Flushes the database and inserts all records from csv files."""

	if not run_silently:
		print "Going to run flush and import all processes."

	_db_flush(run_silently=run_silently)
	_db_import_all(PATH_TO_FILES,run_silently=run_silently)
	
	if not run_silently:
		print "Done with run."
	
	return


def run_view(request):
	"""A wrapper view to be used in urls.py for the run() function."""
	run(run_silently=True)
	return HttpResponse("The import seems to have run without failing! %s" % (time.ctime()))


def _db_flush(run_silently=True):
	"""Deletes data from all wyclif models."""
	
	if not run_silently:
		print "Deleting data from all wyclif models."
	
	# set the models to reset.
	models = [Chapter, Paragraph, Title, Author, Page]

	# flush models.
	for m in models:
		for o in m.objects.all():
			o.delete()

	if not run_silently:
		print "Done deleting data from all wyclif models."


def _db_import_all(PATH_TO_FILES, run_silently=True):
	"""Inserts data into all wyclif models. Calls _db_import() sequentially."""

	# assign John Wyclif to an author id.
	if not run_silently:
		print "Creating database object for Author John Wyclif..."
	wy = Author()
	wy.name = "John Wyclif"
	wy.save()
	if not run_silently:
		print "...done."


	# import rows from csv files.

	# Import book titles.
	if not run_silently:
		print "Importing book titles..."
	_db_import(
		csv_path = PATH_TO_FILES+"tblTitles.csv",
		model = Title,
		field_conversion = {
			# djangofield <- csv
			"text"   : "title"   ,
            "volume" : "volume"  ,
            "pages"  : "pages"   ,
			"old_id" : "titleID" ,
		},
		object_assign = {
			#django field :   assign object
			"author"      :   wy ,  #assign wyclif as author to all.
		},
		run_silently=run_silently,
	)
	if not run_silently:
		print "...Done importing book titles."
	
	
	#import chapters.
	if not run_silently:
		print "Importing chapter information..."
	_db_import(
		csv_path = PATH_TO_FILES+"tblChapters.csv",
		model = Chapter,
		field_conversion = {
			# djangofield    <-  csv
			"old_id"          : "chapterID"    ,
            "xml_chapter_id"  : "xmlChapterID" ,
			"heading"         : "chapterHead"  ,
			"start_page_no"   : "startPageNo"  ,
		},
		query_assign = {
			# djangofield <- { use value for csvfield in csv to get an object from model's modelfield }
			# 		(effectively links models together)
			"title" : {
				"csvfield" : "titleID",
				"get_model" : Title,
				"get_modelfield" : "old_id",
			},
		},
		run_silently=run_silently,
	)
	if not run_silently:
		print "...Done importing chapter information."	
	
	dummy_title = Title(author=wy, volume=0, pages=0)
	dummy_title.save()
	
	dummy_page = Page(title=dummy_title, number=0)
	dummy_page.save()
	
	if not run_silently:
		print "Importing Paragraphs..."
	_db_import(
		csv_path = PATH_TO_FILES+"tblParagraphs.csv",
		model = Paragraph,
		field_conversion = {
			# djangofield <-  csv
			"old_id"      : "paragraphID"   ,
            "number"      : "paragraphNo"   ,
			"old_page_number" : "pageNo"    ,
			"split"       : "split"         ,
			"text"        : "paragraphText" ,
		},
		query_assign = {
			# djangofield <- { use value for csvfield in csv to get an object from model's modelfield }
			# 		(effectively links models together)
			"chapter" : {
				"csvfield" : "chapterID",
				"get_model" : Chapter,
				"get_modelfield" : "old_id",
			},
		},
		object_assign = {
			#django field :   assign object
			"page"      :   dummy_page ,  #assign wyclif as author to all.
		},
		run_silently=run_silently,
	)
	if not run_silently:
		print "...Done importing Paragraphs."
		
	if not run_silently:
		print "Generating new Page information..."
	for paragraph in Paragraph.objects.all():
		model = Page
		
		try:
			page = Page.objects.get(title=paragraph.chapter.title, number=paragraph.old_page_number)
		except Page.DoesNotExist:
			newdata = {
				"title"  : paragraph.chapter.title,
				"number" : paragraph.old_page_number,
				"scan" : None,
			}
			page = model(**newdata)
			page.save()	

		if not run_silently:
			print "%s -> %s" % (newdata,model)
			
		paragraph.page = page
		paragraph.save()
		if not run_silently:
			print "page %s -> paragraph %s" % (page.pk,paragraph.pk)
	
	if not run_silently:
		print "...done generating new Page information."
	
	dummy_title.delete()
	dummy_page.delete()

	#_random_check(dummy_page,dummy_title)
	
	return
	
	
def _db_import(csv_path, model, field_conversion, object_assign=None, query_assign=None, ignore_these_exceptions=None, run_silently=True):
	"""Import data from csv file at csv_path into django model according to field_conversion map."""
	
	#print "_db_import(%s, %s, %s, %s, %s)" % (str(csv_path), str(model), str(field_conversion), str(object_assign), str(query_assign))
	
	dictreader = csv.DictReader(open(csv_path,"r"))
	fieldnames = dictreader.fieldnames
		
	for data in dictreader:
		# Get an array of (newkey, value) pairs.
		# Derive newkey from old fieldnames.
		ar = []
		for djangofield in field_conversion:
			ar.append( (djangofield, unicode( data[field_conversion[djangofield]], errors="ignore" )))
				#errors:
				#1. {'chapterID': '182', 'pageNo': '47', 'paragraphID': '1690', 'paragraphNo': '3', 'paragraphText': 'Similiter talis claustralis ex declinacione a lege domini est sibi valde ingratus, et ut sic indispositus ad orandum. Unde proverb 28o sic scribitur: qui declinat aurem suam ne audiat legem, oracio ejus fiet execrabilis. Similiter ut hic supponitur, justorum sunt omnia et specialiter pauperum spiritu, quantumcunque sint abhominabiles apud mundum: sed clerus dotatus defraudat hos pauperes de sua substancia; igitur propter istam injuriam necesse est deum oracionem illorum repellere, nisi quis blasfemet quod deo ingratus, propter hoc quod est mundo dicior sive excellencior, est pocius in precibus exauditus. Unde in confirmacione istius assumpte sentencie eccci 34o scribitur: qui offert sacrificium de substancia pauperum, quasi qui victimat filium in conspectu patris. Talia sunt multa testimonia in scriptura, ut prov po, ys. po, Malac po, cum aliis. Ex quibus motus fuit beatus gregorius dicere pro prelatis indignis: \xe2\x80\x98Cuncti liquido \xe2\x80\x98novimus cum is qui displicet ad intercedendum mittitur \xe2\x80\x98irati animus proculdubio ad deterius provocatur,\xe2\x80\x99 ut patet in suo pastorali. Et in canone 3a questio 7a si quis in ', 'split': 'top'}
				#     i.e. "\xe2\x80\x98"
				#     'ascii' codec can't decode byte 0xe2 in position 926: ordinal not in range(128)
				#2. {'chapterID': '209', 'pageNo': '104', 'paragraphID': '2310', 'paragraphNo': '3', 'paragraphText': "nullo modo in deterius sibi coaptavit, naturam humanitatis ab eo dignanter assumens, divinitatis ei largitatem tribuens. Illud itaque in verbo, quod in sompno solvitur et in cibo alitur et omnis sentit humanos affectus, hominem persuadet omnibus, quod n\xf2n consumpsit sed assumpsit.' Et sequitur: 'Quidam sibi reddi racionem flagitavit, quomodo deus homini permixtus sit, ut una persona fieret Cristi, cum hoc semel fieri oportuerit. Sed quam racionem reddunt ipsi de re, que cottidie fit, quomodo misceatur anima corpori, ut una persona fiat hominis? Nam sicut in unitate persone anima unitur corpori, ut homo sit, ita in unitate persone deus unitur homini, ut Cristus sit. Ergo in illa persona est mixtura anime et corporis, in hac persona mixtura est dei et hominis: Si tamen recedat auditor a consuetudine corporum, quomodo solent duo liquores ita misceri, ut neutrum integritatem suam servet.' Et eandem sentenciam dicit Augustinus in dyalogo ad Felicianum, et quasi utrobique, ubi swadet infidelibus incarnacionis misterium.", 'split': 'bottom'}
				#     i.e. "\xf2"
				#     'utf8' codec can't decode byte 0xf2 in position 253: invalid continuation byte
		newdata = dict(ar)
	
		if object_assign:
			newdata = dict(newdata.items() + object_assign.items())
	
		if query_assign:
			for djangofield in query_assign:
				query_model = query_assign[djangofield]["get_model"]
				query_modelfield = query_assign[djangofield]["get_modelfield"]
				csvfield = query_assign[djangofield]["csvfield"]
						# look up unicode normalization
				el = query_model.objects.get((query_modelfield , data[csvfield]))
				newdata[djangofield] = el

		try:
			n = model(**newdata)
			n.save()
			nd = n.__dict__

			if not run_silently:
				print "%s -> %s" % (newdata,model)
		except ignore_these_exceptions:
			pass
			
	return


def _random_check(dummy_page, dummy_title):
	
	nc2 = Paragraph.objects.get(chapter__title=dummy_title)
	ncd2 = nc2.__dict__

	nc1 = Paragraph.objects.get(page=dummy_page)
	ncd1 = nc1.__dict__

	raise Exception

