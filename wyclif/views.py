from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext

from wyclif.forms import ParagraphForm, TitleForm, PageForm, ChapterForm


def index(request):
	return render_to_response('wyclif/index.html',
		context_instance=RequestContext(request),
	)
	
def input(request):
	#request_variables = dict(request.REQUEST.items())
	return HttpResponseRedirect('/admin/manuscript/paragraph/add/')
	#return render_to_response('wyclif/input.html')

def input_title(request):
	title_form = TitleForm()

	return render_to_response('wyclif/input.html', {
		'title_form' : title_form,
	})

def input_chapter(request):
	chapter_form = ChapterForm()

	return render_to_response('wyclif/input.html', {
		'chapter_form' : chapter_form,
	})

def input_page(request):
	paragraph_form = ParagraphForm()
	page_form = PageForm()

	return render_to_response('wyclif/input.html', {
		'paragraph_form' : paragraph_form,
		'page_form' : page_form,
	})

def edit_title(request, id):
	try:
		title = Title.objects.get(id=id)
	except Title.DoesNotExist:
		raise Http404

	title_form = TitleForm(title)

	return render_to_response('wyclif/edit.html', {
		'title_form' : title_form,
	})

def edit_chapter(request, id):
	try:
		chapter = Chapter.objects.get(id=id)
	except Chapter.DoesNotExist:
		raise Http404

	chapter_form = ChapterForm(chapter)

	return render_to_response('wyclif/edit.html', {
		'chapter_form' : chapter_form,
	})

def edit_page(request, id):
	try:
		page = Page.objects.get(id=id)
	except Page.DoesNotExist:
		raise Http404

	page_form = PageForm(page)
	paragraphs = Paragraph.objects.filter(page = page)
	paragraph_forms = []
	for paragraph in paragraphs:
		paragraph_forms.append(ParagraphForm(paragraph))
		
	return render_to_response('wyclif/edit.html', {
		'paragraph_forms' : paragraph_forms,
		'page_form' : page_form,
	})

def favicon(request):
	return HttpResponseNotFound()
