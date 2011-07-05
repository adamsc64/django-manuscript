from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound

from wyclif.models import Author, Title, Chapter, Page, Paragraph

def all_works(request):

	works_by_author = []
	

	for author in Author.objects.all():
		works_by_author.append({
			"author" : author,
			"works" : Title.objects.filter(author=author)
		})

	return render_to_response('wyclif/work/all.html', {
		"works_by_author" : works_by_author
	})

def one_work(request, work):
	return render_to_response('wyclif/work/one.html')

def model_by_work(request, work, model):
	return render_to_response('wyclif/work/model_by_work.html')

def element_by_id(request, work, model, id):
	return render_to_response('wyclif/work/element_by_id.html')
