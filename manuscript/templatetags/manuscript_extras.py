# Copyright Christopher Adams, 2011
# All rights reserved.

from django import template

register = template.Library()

from django.conf import settings
from django.utils.safestring import mark_safe

from manuscript.utils import flatten

import re

@register.filter
def highlight(value, arg):
	"""
	Django template that highlights text according to a regular expression.
	For example:
		'{{ foo|highlight:"Pyth.n" }}' -> 'Monty <span class="manuscript-highlighted">Python</span>'
		where foo is "Monty Python"
		and settings.MANUSCRIPT_HIGHLIGHT_CSS_CLASS is "manuscript-highlighted" or is undefined.
	"""
	css_class = settings.MANUSCRIPT_HIGHLIGHT_CSS_CLASS if hasattr(settings,"MANUSCRIPT_HIGHLIGHT_CSS_CLASS") else "manuscript-highlighted"

	full_texts = re.findall(arg, value, flags=re.IGNORECASE)

	# This is necessary for complex return values that come from findall
	# when there are groups in the regexp.
	full_texts = flatten(full_texts)
	while '' in full_texts:
		full_texts.remove('')

	# Reverse sort list of strings from longest to shortest.
	# Avoids tagging smaller results too early, preventing longer results from being
	# replaced.
	full_texts = [(full_text, len(full_text)) for full_text in full_texts]
	full_texts = [s for s, ln in sorted(full_texts, key=lambda ss: -ss[1])]
	
	result = value

	for full_text in full_texts:
		result = result.replace(
			full_text,
			"<span class='%s'>%s</span>" % (css_class,full_text),
		)
	return mark_safe(result)

highlight.is_safe = True

