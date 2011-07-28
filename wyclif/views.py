# Copyright Christopher Adams, 2011
# All rights reserved.

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext

from wyclif.forms import ParagraphForm, TitleForm, PageForm, ChapterForm, BigSearchForm
from manuscript.models import SiteCopyText, Title, Paragraph, Chapter
from manuscript.utils import convert_to_regex_search

def index(request):
	return render(request,'wyclif/index.html')
	
def input(request):
	#request_variables = dict(request.REQUEST.items())
	return HttpResponseRedirect('/admin/manuscript/paragraph/add/')
	#return render_to_response('wyclif/input.html')

def about(request):
	copy_text, created = SiteCopyText.objects.get_or_create_for('about')

	return render(request, 'wyclif/about.html', {
		"copy_text" : copy_text,
	})

def contact(request):
	copy_text, created = SiteCopyText.objects.get_or_create_for('contact')

	return render(request, 'wyclif/contact.html', {
		"copy_text" : copy_text,
	})

def copyright(request):
	url_path = request.META['PATH_INFO']
	copy_text, created = SiteCopyText.objects.get_or_create_for('copyright')

	return render(request, 'wyclif/about.html', {
		"copy_text" : copy_text,
	})


def search(request):
	raw_query = request.GET.get('q')

	if raw_query:
		big_search_form = BigSearchForm(request.GET)
		
		if big_search_form.is_valid():
			q = big_search_form.cleaned_data["q"]
			titles = big_search_form.cleaned_data["titles"]
			
			q = convert_to_regex_search(q)					
			
			if titles:
				paragraph_matches = Paragraph.objects.filter(text__regex=q, chapter__title__in=titles)
			else:
				paragraph_matches = Paragraph.objects.filter(text__regex=q)
				
			chapter_matches = Chapter.objects.filter(heading__regex=q)
		
			return render(request, 'wyclif/works/search.html', {
				"regex_query" : q,
				"big_search_form" : big_search_form,
				"paragraph_matches" : paragraph_matches,
				"chapter_matches" : chapter_matches,
			})
	else:
		big_search_form = BigSearchForm()

	return render(request, 'wyclif/works/search.html', {
		"big_search_form" : big_search_form,
	})


def input_title(request):
	title_form = TitleForm()

	return render(request, 'wyclif/input.html', {
		'title_form' : title_form,
	})

def input_chapter(request):
	chapter_form = ChapterForm()

	return render(request, 'wyclif/input.html', {
		'chapter_form' : chapter_form,
	})

def input_page(request):
	paragraph_form = ParagraphForm()
	page_form = PageForm()

	return render(request, 'wyclif/input.html', {
		'paragraph_form' : paragraph_form,
		'page_form' : page_form,
	})

def edit_title(request, id):
	try:
		title = Title.objects.get(id=id)
	except Title.DoesNotExist:
		raise Http404

	title_form = TitleForm(title)

	return render(request, 'wyclif/edit.html', {
		'title_form' : title_form,
	})

def edit_chapter(request, id):
	try:
		chapter = Chapter.objects.get(id=id)
	except Chapter.DoesNotExist:
		raise Http404

	chapter_form = ChapterForm(chapter)

	return render(request, 'wyclif/edit.html', {
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
		
	return render(request, 'wyclif/edit.html', {
		'paragraph_forms' : paragraph_forms,
		'page_form' : page_form,
	})

def favicon(request):
	return HttpResponseNotFound()

