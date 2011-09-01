# Copyright Christopher Adams, 2011
# All rights reserved.

from manuscript.utils import Prioritizer
import manuscript

def order_titles(queryset):
	"""
	This function takes a django queryset as argument and returns the records
	according to proprietary processing logic.
	"""

	ordered_groups = []
	for pk, text in queryset.values_list('pk','text'):
		orderable_text = text.lower()
		if orderable_text[:3] == 'de ':
			orderable_text = orderable_text[3:]

		ordered_groups.append(
			Prioritizer(
				priority=orderable_text,
				element=queryset.get(pk=pk),
			)
		)

	ordered_groups.sort()
		
	return [item.element for item in ordered_groups]

manuscript.ORDER_TITLES_FN = order_titles