import re
import time

def flatten(l):
	out = []
	for item in l:
		if isinstance(item, (list, tuple)):
		  	out.extend(flatten(item))
		else:
		  	out.append(item)
	return out

class InvalidSearchStringError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

#def execute_search(expr):
#	"""Master function to execute django-manuscript search on an expression.
#	This, and child functions, are in rough shape and need a lot of work."""
#
#	if expr.find(" NEAR ") == -1:
#		execute_near
#
#def execute_near_search(expr):
#	"""Search function to handle NEAR searches."""

def convert_to_regex_search(expr):
	"""function to handle regular expression searches for AND and OR."""
	
	expr = expr.replace("(","~")
	expr = expr.replace(")","%")
	
	def __finder(expr):
		regex = re.compile(r"\~[^\(\)]+\%", re.IGNORECASE)
		match = regex.search(expr)
		if match:
			sub_expr = match.group()
			result = __finder(expr.replace(sub_expr, str(__finder(sub_expr[1:-1]))))
			return result
		result = _parse_search(expr)
		return result

	return __finder(expr)

def _parse_search(q):

	q = q.replace("*","\w*")
	ORs = q.split(" OR ")
	
	or_list = []
	
	for OR in ORs:
		ANDs = OR.split(" AND ")
		if len(ANDs) > 1:
			conditions = []
			for i in range(len(ANDs)):
				word1 = ANDs[i].strip()
				if word1 == "" or word1 == "\w*":
					raise InvalidSearchStringError(q)
				for j in range(i,len(ANDs)):
					word2 = ANDs[j].strip()
					if word2 == "" or word2 == "\w*":
						raise InvalidSearchStringError(q)
					if word1 != word2:
						print word1, word2
						conditions.append(_full_word_regex(word1 + ".*" + word2))
						conditions.append(_full_word_regex(word2 + ".*" + word1))
		else:
			word = ANDs[0]
			if word == "" or word == "\w*":
				raise InvalidSearchStringError(q)
			word = _full_word_regex(word)
			conditions = [word]
				
		or_list.append("|".join("(%s)" % condition for condition in conditions))
		
		regex = ("(%s)" % "|".join(o for o in or_list)) if len(or_list)>1 else or_list[0]
	
	return regex

def _full_word_regex(word):
	return r"\b%s\b" % word

SEARCH_ENCODING = (
    # (starting value, temporary value, regex equivalent)
    ("*","WILDCARD","[A-Za-z0-9]*"),
)
def clean_for_search_parser(q):
    for start, temp, regex in SEARCH_ENCODING:
        q = q.replace(start,temp)
    return q
def make_wildcards_regex(word):
    for start, temp, regex in SEARCH_ENCODING:
        word = word.replace(temp,regex)
    return word

class Prioritizer:
    """This class effectively sorts displays information, sortable by 'priority' field."""
    def __init__(self,priority,**args):
        self.priority=priority
        for i in args:
            setattr(self,i,args[i])
    def __cmp__(self,other):
        return cmp(self.priority, other.priority)


class Word(object):
	"""
	This class is used by the search engine to find the relationships between
	words within logical paragraphs. For example, distance between words, or
	finding words within the same paragraph. It takes care of the fact that
	logical paragraphs within the manuscript django application may be spread
	across two or more objects within the manuscript.paragraph model.
	"""

	def __init__(self, paragraph, word_index):
		if not paragraph:
			raise Exception("Invalid paragraph: %s" % paragraph)
		if word_index != 0 and not word_index:
			raise Exception("Invalid word_index: %s" % word_index)

		self._paragraph = paragraph
		
		self._paragraph_words = unicode(self._paragraph.text).split(" ")
		self._word = self._paragraph_words[word_index]

		self._word_index = word_index % len(self._paragraph_words) # sets correctly if -1
		
	def __str__(self):
		return str(self._word)

	def __unicode__(self):
		return unicode(self._word)

	def __repr__(self):
		return "Word(%s, %s) == \"%s\"" % (self._paragraph, self._word_index, unicode(self))
		
	def __eq__(self,other):
		if hasattr(other, "_paragraph"):
			if self._paragraph.pk == other._paragraph.pk:
				if self._word_index == other._word_index:
					return True
		return False
	
	def is_first_in_paragraph(self):
		return self._word_index == 0
		
	def is_last_in_paragraph(self):
		return self._word_index == len(self._paragraph_words) - 1
	
	def get_paragraph(self):
		return self._paragraph

	def previous(self, jump=1):
		"""
		Returns the previous logical Word object.
		"""
		if jump == 0:
			return self
			
		if jump < 0:
			return self.next(jump=-jump)

		if self._word_index-jump >= 0:
			return Word(self._paragraph, self._word_index-jump)

		if jump > 1:
			recurs = self.previous(jump-1)
			if recurs:
				return recurs.previous()
			else:
				return None

		#jump == 1
		
		if self.is_first_in_paragraph():
			prev_paragraph = self._paragraph.previous()
			if prev_paragraph:
				return prev_paragraph.last_word()
			else:
				return None
		else:
			return Word(
				self._paragraph,
				self._word_index - jump,
			)
	
	def next(self, jump=1):
		"""
		Returns the next logical Word object.
		"""
		if jump == 0:
			return self
			
		if jump < 0:
			return self.previous(jump=-jump)

		if self._word_index+jump < len(self._paragraph_words):
			return Word(self._paragraph, self._word_index+jump)

		if jump > 1:
			recurs = self.next(jump-1)
			if recurs:
				return recurs.next()
			else:
				return None

		#jump == 1

		if self.is_last_in_paragraph():
			next_paragraph = self._paragraph.next()
			if next_paragraph:
				return next_paragraph.first_word()
			else:
				return None
		else:
			return Word(
				self._paragraph,
				self._word_index + jump,
			)


	def test(self, count=10):
		w1 = self.next(jump=count)
		w2 = self
		for i in range(count):
			print "word[%s] = %s" % (i, w2)
			w2 = w2.next()
		
		print "%s == %s : %s " % (w1, w2, w1==w2)


	def print_and_follow(self):
		"""
		For testing.
		"""
		w1 = self
		while w1:
			print w1
			w1=w1.next()
			time.sleep(.5)
		
	
	def previous_few(self, count):
		result = []
		for i in range(1, count+1):
			previous = self.previous(jump=i)
			if previous:
				result.insert(0, previous)
		return result

	def next_few(self, count):
		result = []
		for i in range(1, count+1):
			next = self.next(jump=i)
			if next:
				result.append(next)
		return result
	
	def get_nearby(self, distance=0):
		"""
		Finds and returns the nearby Word objects by `distance` from this word.
		Default returns only this word.
		"""
		result = []
		
		result = result + self.previous_few(distance)
		result = result + [self,]
		result = result + self.next_few(distance)

		return result

def is_near(word1, word2, num_words):
	"""
	Returns an array of unique paragraph objects that have these words
	near each other.
	"""
	
	word1 = unicode(word1)
	word2 = unicode(word2)
	
	from manuscript.models import Paragraph
	
	paragraphs_for1 = \
		Paragraph.objects.filter(text__icontains=unicode(word1+u" ")) | \
		Paragraph.objects.filter(text__icontains=unicode(u" "+word1))
		
	words = []
	
	for p in paragraphs_for1:
		print "Searching paragraph %s" % p.pk
		words.extend(p.get_words_for(word1))
		print " found %s in paragraph %s" % (word1, p.pk)

	result = []
	
	for result_word1 in words:
		for nearby in result_word1.get_nearby(distance=num_words):
			if unicode(nearby) == unicode(word2):
				print "%s is near %s" % (nearby, result_word1)
				result.append(nearby._paragraph.pk)
				result.append(result_word1._paragraph.pk)
			
	result = list(set(result))
	
	return Paragraph.objects.filter(pk__in=result)
	

def get_random_word():
	"""
	For testing purposes.
	"""
	from manuscript.models import Paragraph
	l = Paragraph.objects.all().count()

	from random import random
	i = int(l * random())
	p = Paragraph.objects.all()[i]
	return Word(p,0)