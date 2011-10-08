# Copyright Christopher Adams, 2011
# All rights reserved.

from manuscript.utils import Prioritizer
from manuscript.models import Title
import manuscript

import re

def text_to_sort_by(self):
	CUT_OUT = [
		"^De\ ",
		"^Sermones\ ",
		"^[IVXLCDM]*\ ",
	]
	for regexp in CUT_OUT:
		result = re.split(regexp, self.text)
		if len(result) > 1: #There is a match
			return result[1]
	return self.text

Title.text_to_sort_by = text_to_sort_by
