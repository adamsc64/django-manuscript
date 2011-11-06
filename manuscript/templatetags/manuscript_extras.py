# Copyright (C) 2011 by Christopher Adams
# Released under MIT License. See LICENSE.txt in the root of this
# distribution for details.

from django import template

register = template.Library()

from django.conf import settings
from django.utils.safestring import mark_safe

from manuscript.utils import flatten

import re

@register.filter
def highlight(value, arg):
	"""
	Django template tag that highlights parts of words according to regex patterns in a list.
	For example:
		'{{ foo|highlight:lst }}' -> 'Monty <span class="manuscript-highlighted">Python</span>'
		where foo is "Monty Python" and lst = ["pyth.n"]
		and settings.MANUSCRIPT_HIGHLIGHT_CSS_CLASS is "manuscript-highlighted" or is undefined.
	"""
	result = value
	regexs = arg

	if regexs==None:
		return result

	css_class = settings.MANUSCRIPT_HIGHLIGHT_CSS_CLASS if hasattr(settings,"MANUSCRIPT_HIGHLIGHT_CSS_CLASS") else "manuscript-highlighted"

	for regex in regexs:
		full_texts = re.findall(regex, result, flags=re.IGNORECASE)

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
	
		for full_text in full_texts:
			result = result.replace(
				full_text,
				"<span class='%s'>%s</span>" % (css_class,full_text),
			)
			
	return mark_safe(result)

highlight.is_safe = True

