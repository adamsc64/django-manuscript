# Copyright Christopher Adams, 2011
# All rights reserved.

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q

from manuscript.models import Author, Title, Chapter, Page, Paragraph, SiteCopyText

def all_works(request):	
	copy_text, created = SiteCopyText.objects.get_or_create_for('all_works')

	works_by_author = []

	for author in Author.objects.all():
		works_by_author.append({
			"author" : author,
			"works" : Title.objects.filter(author=author)
		})

	return render(request, 'wyclif/works/all-titles.html', {
		"works_by_author" : works_by_author,
		"copy_text" : copy_text,
	})


def chapters(request, title):
	copy_text, created = SiteCopyText.objects.get_or_create_for('chapters')

	try:
		title = Title.objects.get(slug=title)
	except Title.DoesNotExist:
		raise Http404
	
	return render(request, 'wyclif/works/chapters.html', {
		"copy_text" : copy_text,
		"title" : title,
	})
	
def paragraphs(request, title, chapter):
	copy_text, created = SiteCopyText.objects.get_or_create_for('paragraphs')

	try:
		title = Title.objects.get(slug=title)
		chapter = title.chapter_set.get(slug=chapter)
	except Title.DoesNotExist, Chapter.DoesNotExist:
		raise Http404
	
	return render(request, 'wyclif/works/paragraphs.html', {
		"copy_text" : copy_text,
		"title" : title,
		"chapter" : chapter,
	})

def chapter(request, title, chapter):
	try:
		title = Title.objects.get(slug=title)
		chapter = title.chapter_set.get(slug=chapter)
		page = chapter.paragraph_set.filter(~Q(split="bottom")).order_by('number')[0].page
	except Title.DoesNotExist, Chapter.DoesNotExist:
		raise Http404
		
	return HttpResponseRedirect(reverse('show-page', args=(title.slug, page.number)))

def page(request, title, page):
	copy_text, created = SiteCopyText.objects.get_or_create_for('page')

	try:
		title = Title.objects.get(slug=title)
		page = Page.objects.get(title=title, number=page)
	except Title.DoesNotExist, Page.DoesNotExist:
		raise Http404

	paragraphs = page.paragraph_set.all().order_by('number')
	chapters = paragraphs.values_list('chapter',flat=True)
	chapters = Chapter.objects.filter(pk__in=chapters)		

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
	
	return render(request, 'wyclif/works/page.html', {
		"copy_text" : copy_text,
		"title" : title,
		"page" : page,
		"page_first" : page_first, "page_last" : page_last,
		"page_prev" : page_prev, "page_next" : page_next,
		"paragraphs" : paragraphs,
		"chapters" : chapters,
	})
	