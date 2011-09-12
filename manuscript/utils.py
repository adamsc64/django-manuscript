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
		self._paragraph = paragraph
		
		self._paragraph_words = unicode(self._paragraph.text).split(" ")
		self._word = self._paragraph_words[word_index]

		self._word_index = word_index % len(self._paragraph_words) # sets correctly if -1
	
	def __str__(self):
		return unicode(self._word)

	def __repr__(self):
		return "Word(%s, %s)" % (self._paragraph, self._word_index)
		
	def __eq__(self,other):
		if self._paragraph.pk == other._paragraph.pk:
			if self._word_index == other._word_index:
				return True
		return False
	
	def get_paragraph(self):
		return self._paragraph

	def previous(self, jump=1):
		if not self._word_index-jump < 0:
			return Word(self._paragraph, self._word_index-jump)
		else:
			return Word(self._paragraph.previous(), self._word_index-jump)
	
	def next(self, jump=1):
		"""
		Returns the next logical Word object.
		"""
		if self._word_index+jump < len(self._paragraph_words):
			return Word(self._paragraph, self._word_index+jump)
		else:
			next_paragraph = this_paragraph = self._paragraph
			next_paragraph_words = self._paragraph_words
			this_index = self._word_index
			next_index = None

			while next_index == None or next_index >= len(next_paragraph_words):
				old_paragraph = this_paragraph
				this_paragraph = next_paragraph
				this_paragraph_words = next_paragraph_words

				next_paragraph = old_paragraph.next()
				if next_paragraph:
					next_paragraph_words = unicode(next_paragraph.text).split(" ")

					old_index = this_index
					this_index = next_index
					next_index = old_index + jump - len(this_paragraph_words)
				else:
					return None
			
			return Word(
				next_paragraph,
				next_index,
			)

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
		for i in range(1, count):
			result.insert(0, self.previous(jump=i))
		return result

	def next_few(self, count):
		result = []
		for i in range(1, count):
			result.append(self.next(jump=i))
		return result
	
	def find_nearby(self, distance=0):
		"""
		Finds and returns the nearby Word objects by `distance` from this word.
		Default returns only this word.
		"""
		result = []
		
		result = result + self.previous_few(distance)
		result = result + [self,]
		result = result + self.next_few(distance)

		return result

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