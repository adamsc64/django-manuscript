"""Module to import sample csv data into model. Use run() at commandline or run_view() in urls.py."""

import csv
import os
import time

from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse

from Wyclif.models import Chapter, Paragraph, Title, Author, Page


def run(PATH_TO_FILES = os.path.dirname(os.path.abspath(__file__)) + os.sep): # "/Users/chris/coding/wyclif_project/Wyclif/lib/Wyclif/bin/"
	"""Flushes the database and inserts all records from csv files."""
	_db_flush()
	_db_import_all(PATH_TO_FILES)
	return


def run_view(request):
	"""A wrapper view to be used in urls.py for the run() function."""
	run()
	return HttpResponse("The import seems to have run without failing! %s" % (time.ctime()))


def _db_flush():
	"""Deletes data from all Wyclif models."""
	
	# set the models to reset.
	models = [Chapter, Paragraph, Title, Author, Page]

	# flush models.
	for m in models:
		for el in m.objects.all():
			el.delete()


def _db_import_all(PATH_TO_FILES):
	"""Inserts data into all Wyclif models. Calls _db_import() sequentially."""

	# assign John Wyclif to an author id.
	wy = Author()
	wy.name = "John Wyclif"
	wy.save()

	# import rows from csv files.

	# Import book titles.
	_db_import(
		csv_path = PATH_TO_FILES+"tblTitles.csv",
		model = Title,
		conversion = {
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
	)
	
	#import chapters.
	_db_import(
		csv_path = PATH_TO_FILES+"tblChapters.csv",
		model = Chapter,
		conversion = {
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
	)

	#autopopulate the Page model with dummy pages for each Title object.

	def _db_assign_foreach( item_in, set_field, in_model, assign_range, to_field ):
		for item in item_in:
			for i in assign_range:
				args = {
					set_field : item,
					to_field : i,
				}
				print "Creating new %s with %s" % (in_model, args)
				in_model(**args).save()		

	_db_assign_foreach(
		item_in = Title.objects.all(),
		set_field = "title", in_model = Page, 
		assign_range = range(0,1000),
		to_field = "number",
	)

	#import pages (get from paragraphs data.)
	#_db_import(
	#	csv_path = PATH_TO_FILES+"tblParagraphs.csv",
	#	model = Page,
	#	conversion = {
	#		# djangofield <-  csv
	#		"number"      : "pageNo" 
	#	},
	#	query_assign = {
	#		# djangofield <- { use value for csvfield in csv to get an object from model's modelfield }
	#		# 		(effectively links models together)
	#		"title" : {
	#			"csvfield" : "chapterID",
	#			"get_model" : Chapter,
	#			"get_modelfield" : "old_id",
	#		},
	#	},
		

		#ignore_these_exceptions = (
		#	IntegrityError,
		#)
	#)
	_db_import(
		csv_path = PATH_TO_FILES+"tblParagraphs.csv",
		model = Paragraph,
		conversion = {
			# djangofield <-  csv
			"old_id"      : "paragraphID"   ,
            "number"      : "paragraphNo"   ,
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
			"page" : {
				"csvfield" : "pageNo",
				"get_model" : Page,
				"get_modelfield" : "number",
			},
		},
	)
	
def _db_import(csv_path, model, conversion, object_assign=None, query_assign=None, ignore_these_exceptions=None):
	"""Import data from csv file at csv_path into django model according to conversion map."""
	
	print "_db_import(%s, %s, %s, %s, %s)" % (str(csv_path), str(model), str(conversion), str(object_assign), str(query_assign))
	
	dictreader = csv.DictReader(open(csv_path,"r"))
	fieldnames = dictreader.fieldnames
		
	for data in dictreader:
		# Get an array of (newkey, value) pairs.
		# Derive newkey from old fieldnames.
		ar = []
		for djangofield in conversion:
			ar.append( (djangofield, unicode( data[conversion[djangofield]], errors="replace" )))
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
			model(**newdata).save()
		except ignore_these_exceptions:
			pass
			
	return
