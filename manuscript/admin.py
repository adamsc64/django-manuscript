# Copyright (C) 2011 by Christopher Adams
# Released under MIT License. See LICENSE.txt in the root of this
# distribution for details.

from django.contrib import admin

from manuscript.models import Chapter, Paragraph, Title, Author, Page, SiteCopyText, CompositeParagraph

admin.site.register(Chapter,
	list_display = ('title','heading','start_page_no'),
	list_display_links = ('heading',),
	list_filter = ('title',),
	search_fields = ['heading','start_page_no'],
	
	fields = ('title','slug','heading','start_page_no','get_children_links'),
	readonly_fields = ('slug','get_children_links',),
)
admin.site.register(Paragraph,
	list_display = ('title','chapter','number','page','split','text'),
	list_display_links = ('number','text'),
	list_filter = ('page',),
	search_fields = ['number','text'],
	
	fields = ('page','chapter','number','split','text'),
)
admin.site.register(CompositeParagraph,
	fields = ('chapter','number','pages','text','get_children_links'),
	readonly_fields = ('get_children_links',),
)
admin.site.register(Title,
	list_display = ('text','volume','pages'),
	list_display_links = ('text','volume'),
	search_fields = ['text','volume'],

	fieldsets = (
		("Basic Information", {
			'fields' : (
				'text','author',
			)
		}),
		("Bibliographic Information", {
			'fields' : (
				'volume','num_volumes','editor','publisher',
				'place_of_publication','publication_year','pages',
			)
		}),
		("Special Beginning Pages", {
			'fields' : (
				'title_page','copyright_page',
			)
		}),
		("URL display settings", {
			'fields' : (
				'slug',
			)
		}),
		("Reprinting Information", {
			'fields' : (
				'if_a_reprint_original_publication_information',
			)
		}),
		("Chapters", {
			'fields' : (
				'get_children_links',
			)
		}),
	),
	readonly_fields = ('slug','get_children_links',),
)
admin.site.register(Author)

admin.site.register(Page,
	list_display = ('title','number','scan'),
	list_display_links = ('number',),
	list_filter = ('title',),
	search_fields = ['number',],

	fields = ('title','number','scan','get_children_links'),
	readonly_fields = ('get_children_links',),
)

admin.site.register(SiteCopyText,
	list_display = ('index','value'),
	list_display_links = ('index','value'),
)
