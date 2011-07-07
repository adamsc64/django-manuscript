from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext

from wyclif.models import Author, Title, Chapter, Page, Paragraph, SiteCopyText

def all_works(request):
	
	copy_text, created = SiteCopyText.objects.get_or_create(
		index="wyclif.works.all_works",
		defaults={'value' : "Editable text to introduce all works."}
	)

	works_by_author = []

	for author in Author.objects.all():
		works_by_author.append({
			"author" : author,
			"works" : Title.objects.filter(author=author)
		})

	return render_to_response('wyclif/work/all-works.html', {
		"works_by_author" : works_by_author,
		"copy_text" : copy_text,
	},
		context_instance=RequestContext(request),
	)


def chapters(request, title):
	
	copy_text, created = SiteCopyText.objects.get_or_create(
		index="wyclif.works.chapters",
		defaults={'value' : "Editable text to introduce chapters."}
	)
	
	try:
		title = Title.objects.get(slug=title)
	except Title.DoesNotExist:
		raise Http404
	
	return render_to_response('wyclif/work/chapters.html', {
		"copy_text" : copy_text,
		"title" : title,
	},
		context_instance=RequestContext(request),
	)
	
def pages(request, title, chapter):

	copy_text, created = SiteCopyText.objects.get_or_create(
		index="wyclif.works.pages",
		defaults={'value' : "Editable text to introduce all pages."}
	)

	try:
		title = Title.objects.get(slug=title)
		chapter = title.chapter_set.get(slug=chapter)
	except Title.DoesNotExist, Chapter.DoesNotExist:
		raise Http404
	
	return render_to_response('wyclif/work/pages.html', {
		"copy_text" : copy_text,
		"title" : title,
		"chapter" : chapter,
	},
		context_instance=RequestContext(request),
	)



def one_work(request, work):
	return render_to_response('wyclif/work/one.html')

def model_by_work(request, work, model):
	return render_to_response('wyclif/work/model_by_work.html')

def element_by_id(request, work, model, id):
	return render_to_response('wyclif/work/element_by_id.html')
