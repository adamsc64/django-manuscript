# Copyright Christopher Adams, 2011
# All rights reserved.

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
	list_display = ('text','volume','publication_year','pages'),
	list_display_links = ('text','volume'),
	search_fields = ['text','volume'],

	fields = ('text','slug','volume','publication_year','pages','author','get_children_links'),
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
