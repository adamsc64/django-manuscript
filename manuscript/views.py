from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q

import re

from manuscript.models import Author, Title, Chapter, Page, Paragraph, SiteCopyText
from manuscript.models import compile_paragraphs

from manuscript.utils import convert_to_regex_search, clean_for_search_parser, make_wildcards_regex
from manuscript.utils import InvalidSearchStringError, is_near
from manuscript.utils import flatten
from manuscript.searchparser import SearchQueryParser
from manuscript.forms import BigSearchForm

def all_works(request):	
	copy_text, created = SiteCopyText.objects.get_or_create_for('all_works')

	works_by_author = []

	for author in Author.objects.all():

		works = sorted(
			Title.objects_with_data.filter(author=author),
			key=Title.text_to_sort_by
		)

		works_by_author.append({
			"author" : author,
			"works" :  works,
		})

	return render(request, 'manuscript/all-titles.html', {
		"works_by_author" : works_by_author,
		"copy_text" : copy_text,
	})

def whole_work(request, title):
	copy_text, created = SiteCopyText.objects.get_or_create_for('whole_work')

	try:
		title = Title.objects.get(slug=title)
	except Title.DoesNotExist:
		raise Http404

	all_chapters = title.chapter_set.all()

	chapter_datasets = []

	for chapter in all_chapters:
		paragraphs = chapter.get_paragraph_strings()
		chapter_datasets.append([
			chapter,
			paragraphs,
		])

	return render(request, 'manuscript/whole-work.html', {
		"title" : title,
		"all_chapters" : all_chapters,
		"chapter_datasets" : chapter_datasets,
	})

def chapters(request, title):
	copy_text, created = SiteCopyText.objects.get_or_create_for('chapters')

	try:
		focus_title = Title.objects.get(slug=title)
	except Title.DoesNotExist:
		raise Http404
		
	all_titles = sorted(
		Title.objects_with_data.all(),
		key=Title.text_to_sort_by
	)
	
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
	
	highlight = request.GET.get('highlight')
	
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
		"regex_query" : highlight,
	})


def recreate_paragraph_composites(request):
	compile_paragraphs(flush=True)
	return HttpResponse("Seems to have run ok.")


def search(request):
    raw_query = request.GET.get('q')

    if raw_query:
        big_search_form = BigSearchForm(request.GET)

        if big_search_form.is_valid():
            original_q = big_search_form.cleaned_data["q"]
            cleaned_q = clean_for_search_parser(original_q)
            titles = big_search_form.cleaned_data["titles"]

            # This needs to be much better.
            if cleaned_q.find(" NEAR ") != -1:
                NEARs = cleaned_q.split(" NEAR ")
                if len(NEARs) > 1:
                    NEARs[0] = NEARs[0].strip()
                    NEARs[1] = NEARs[1].strip()
                    #matches1 = Paragraph.objects.filter(text__icontains=str(NEARs[0]))
                    #matches2 = Paragraph.objects.filter(text__icontains=str(NEARs[1]))
                    #
                    #by_words = request.GET.get('nearprompt')
                    #
                    #q = r"\b(?:%s\W+(?:\w+\W+){1,%s}?%s|%s\W+(?:\w+\W+){1,%s}?%s)\b" % \
                    #   (NEARs[0], by_words, NEARs[1], NEARs[1], by_words, NEARs[0])
                    #regex = re.compile(q, re.IGNORECASE)
                    #
                    #paragraph_matches = Paragraph.objects.filter(text__iregex=q)

                    by_words = request.GET.get('nearprompt')
                    if by_words:
                        paragraph_matches = is_near(NEARs[0] , NEARs[1], num_words=int(by_words))
                    else:
                        paragraph_matches = Paragraph.objects.none()                        
                else:
                    paragraph_matches = Paragraph.objects.none()

                if titles:
                    paragraph_matches = paragraph_matches.filter(chapter__title__in=titles)
            else:
                try:
                    parse = SearchQueryParser().parser()

                    # Load all paragraph data into RAM.
                    # We could, alternatively, compile a __regex filter search,
                    # but the syntax of __regex is database-backend dependent.
                    # This is better because it runs regex search at the
                    # python level.
                    paragraphs = Paragraph.objects.all()

                    def understand(o):
                        numkeys = len(o.keys())

                        result_ids = []

                        unary_func = [
                            "word", "quotes"
                        ]
                        binary_func = {
                            "or" : "union",
                            "and": "intersection",
                        }

                        def _django_query(o,operator):
                            if operator == "word":
                                matchme = o[0]
                            elif operator == "quotes":
                                elements = o.asList()
                                matchme = " ".join(flatten(elements))

                            matchme = make_wildcards_regex(matchme)
                            matchme = matchme.lower()
                            pattern = "\\b" + matchme + "\\b"

                            for paragraph in paragraphs:
                                if re.search(pattern, paragraph.text, re.IGNORECASE):
                                    result_ids.append(paragraph.pk)
                            result = set(result_ids)
                            return result

                        if numkeys == 0 and o.asDict() == {}:
                            operator = o.getName()
                            return _django_query(o,operator)
                        elif numkeys == 1:
                            #initial run.
                            operator = o.keys().pop().lower()

                            next = o[operator]

                            if operator in binary_func:
                                next1, next2 = next
                                set1 = understand(next1)
                                set2 = understand(next2)
                                result = getattr(set1,binary_func[operator])(set2)
                                return result
                            elif operator in unary_func:
                                return _django_query(next,operator)
                            else:
                                raise InvalidSearchStringError("Unknown operator %s" % operator)
                        else:
                            raise InvalidSearchStringError("Something went wrong with keys in pyparsing search.")

                    id_matches = understand(parse(cleaned_q))
                    paragraph_matches = paragraphs.filter(id__in=list(id_matches))

                except InvalidSearchStringError:
                    paragraph_matches = Paragraph.objects.none()
                else:
                    if titles:
                        paragraph_matches = paragraph_matches.filter(chapter__title__in=titles)

            # Sort paragraph_matches by title.
            results_by_title = []
            for title in Title.objects.all():
                paragraphs_in_title = paragraph_matches.filter(page__title=title)
                pair = title,paragraphs_in_title
                if paragraphs_in_title.count() > 0:
                    results_by_title.append(pair)


            return render(request, 'manuscript/search.html', {
                "regex_query" : raw_query,
                "big_search_form" : big_search_form,
                "results_by_title" : results_by_title,
                "num_results" : paragraph_matches.count()
            })
    else:
        big_search_form = BigSearchForm()

    return render(request, 'manuscript/search.html', {
        "big_search_form" : big_search_form,
    })
