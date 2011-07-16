from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext

from manuscript.models import Author, Title, Chapter, Page, Paragraph, SiteCopyText

def all_works(request):	
	copy_text, created = SiteCopyText.objects.get_or_create_for('all_works')

	works_by_author = []

	for author in Author.objects.all():
		works_by_author.append({
			"author" : author,
			"works" : Title.objects.filter(author=author)
		})

	return render_to_response('wyclif/work/all-titles.html', {
		"works_by_author" : works_by_author,
		"copy_text" : copy_text,
	},
		context_instance=RequestContext(request),
	)


def chapters(request, title):
	copy_text, created = SiteCopyText.objects.get_or_create_for('chapters')

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
	
def paragraphs(request, title, chapter):
	copy_text, created = SiteCopyText.objects.get_or_create_for('paragraphs')

	try:
		title = Title.objects.get(slug=title)
		chapter = title.chapter_set.get(slug=chapter)
	except Title.DoesNotExist, Chapter.DoesNotExist:
		raise Http404
	
	return render_to_response('wyclif/work/paragraphs.html', {
		"copy_text" : copy_text,
		"title" : title,
		"chapter" : chapter,
	},
		context_instance=RequestContext(request),
	)

def page(request, title, page):
	copy_text, created = SiteCopyText.objects.get_or_create_for('page')

	try:
		title = Title.objects.get(slug=title)
		page = Page.objects.get(title=title, number=page)
	except Title.DoesNotExist, Page.DoesNotExist:
		raise Http404
	
	return render_to_response('wyclif/work/page.html', {
		"copy_text" : copy_text,
		"title" : title,
		"page" : page,
	},
		context_instance=RequestContext(request),
	)
	