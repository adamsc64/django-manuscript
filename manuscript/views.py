from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q

from manuscript import ORDER_TITLES_FN as order_titles
from manuscript.models import Author, Title, Chapter, Page, Paragraph, SiteCopyText
from manuscript.models import compile_paragraphs


def all_works(request):	
	copy_text, created = SiteCopyText.objects.get_or_create_for('all_works')

	works_by_author = []

	for author in Author.objects.all():

		works = order_titles(Title.objects.filter(author=author))

		works_by_author.append({
			"author" : author,
			"works" :  works,
		})

	return render(request, 'manuscript/all-titles.html', {
		"works_by_author" : works_by_author,
		"copy_text" : copy_text,
	})


def chapters(request, title):
	copy_text, created = SiteCopyText.objects.get_or_create_for('chapters')

	try:
		focus_title = Title.objects.get(slug=title)
	except Title.DoesNotExist:
		raise Http404
		
	all_titles = order_titles(Title.objects.all())
	
	return render(request, 'manuscript/chapters.html', {
		"copy_text" : copy_text,
		"focus_title" : focus_title,
		"all_titles" : all_titles,
	})
	
def paragraphs(request, title, chapter):
	copy_text, created = SiteCopyText.objects.get_or_create_for('paragraphs')

	try:
		title = Title.objects.get(slug=title)
		chapter = title.chapter_set.get(slug=chapter)
	except Title.DoesNotExist:
		raise Http404
	except Chapter.DoesNotExist:
		raise Http404
	
	return render(request, 'manuscript/paragraphs.html', {
		"copy_text" : copy_text,
		"title" : title,
		"chapter" : chapter,
	})

def chapter(request, title, chapter):
	try:
		title = Title.objects.get(slug=title)
		chapter = title.chapter_set.get(slug=chapter)
		#page = chapter.paragraph_set.filter(~Q(split="bottom")).order_by('number')[0].page
	except Title.DoesNotExist:
		raise Http404
	except Chapter.DoesNotExist:
		raise Http404
	
	paragraphs = chapter.get_paragraph_strings()
	all_chapters = title.chapter_set.all()
	
	return render(request, 'manuscript/chapter.html', {
		"title" : title,
		"chapter" : chapter,
		"all_chapters" : all_chapters,
		"paragraphs" : paragraphs,
	})

def page(request, title, page):
	copy_text, created = SiteCopyText.objects.get_or_create_for('page')

	try:
		title = Title.objects.get(slug=title)
		page = Page.objects.get(title=title, number=page)
	except Title.DoesNotExist:
		raise Http404
	except Page.DoesNotExist:
		raise Http404		

	paragraphs = page.paragraph_set.all().order_by('chapter__start_page_no','number')
	if paragraphs.count() > 0:
		focus_chapter = paragraphs.reverse()[0].chapter
		focus_chapter_first_paragraph = focus_chapter.paragraph_set.all().order_by('number')[0]
	else:
		focus_chapter = None
		focus_chapter_first_paragraph = None

	all_chapters = title.chapter_set.all()

	page_first = Page.objects.filter(title=page.title).order_by('number')[0]
	page_last = Page.objects.filter(title=page.title).order_by('-number')[0]

	try:
		page_prev = Page.objects.get(title=page.title, number=page.number-1)
	except Page.DoesNotExist:
		page_prev = None
	
	try:
		page_next = Page.objects.get(title=page.title, number=page.number+1)
	except Page.DoesNotExist:
		page_next = None
	
	return render(request, 'manuscript/page.html', {
		"copy_text" : copy_text,
		"title" : title,
		"page" : page,
		"page_first" : page_first, "page_last" : page_last,
		"page_prev" : page_prev, "page_next" : page_next,
		"paragraphs" : paragraphs,
		"focus_chapter" : focus_chapter,
		"focus_chapter_first_paragraph" : focus_chapter_first_paragraph,
		"all_chapters" : all_chapters,
	})


def recreate_paragraph_composites(request):
	compile_paragraphs(flush=True)
	return HttpResponse("Seems to have run ok.")