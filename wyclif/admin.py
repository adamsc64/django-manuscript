from django.contrib import admin

from wyclif.models import Chapter,Paragraph,Title,Author,Page

admin.site.register(Chapter,
	list_display = ('title','heading','start_page_no'),
	list_display_links = ('heading',),
	list_filter = ('title',),
	search_fields = ['heading','start_page_no'],
	
	fields = ('title','heading','start_page_no','get_children_links'),
	readonly_fields = ('get_children_links',),
)
admin.site.register(Paragraph,
	list_display = ('title','chapter','number','page','split','text'),
	list_display_links = ('number','text'),
	search_fields = ['number','text'],
)
admin.site.register(Title,
	list_display = ('text','volume','pages'),
	list_display_links = ('text','volume'),
	search_fields = ['text','volume'],

	fields = ('text','volume','pages','author','get_children_links'),
	readonly_fields = ('get_children_links',),
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
