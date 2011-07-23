from django import template

register = template.Library()

from django.conf import settings
from django.utils.safestring import mark_safe


@register.filter
def highlight(value, arg):
	"""
	Django template that highlights text.
	For example:
		'{{ foo|highlight:"Python" }}' -> 'Monty <span class="manuscript-highlighted">Python</span>'
		where foo is "Monty Python"
		and settings.MANUSCRIPT_HIGHLIGHT_CSS_CLASS is "manuscript-highlighted" or is undefined.
	"""
	css_class = settings.MANUSCRIPT_HIGHLIGHT_CSS_CLASS if hasattr(settings,"MANUSCRIPT_HIGHLIGHT_CSS_CLASS") else "manuscript-highlighted"
	return mark_safe(
		value.replace(
			arg,
			"<span class='%s'>%s</span>" % (css_class,arg)
		)
	)

highlight.is_safe = True
