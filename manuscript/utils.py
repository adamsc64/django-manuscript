from manuscript.searchparser import SearchQueryParser

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

def execute_search(cleaned_q, titles, near_by_words):
    """
    Master function to execute django-manuscript search on an expression.
    This, and child functions, can still use some work.
    """
    
    from manuscript.models import Paragraph, Title
    
    parse = SearchQueryParser().parser() # returns a callable.
    near_by_words = int(near_by_words) if near_by_words else None
    
    is_near_search = near_by_words and re.findall("^(\w*)\snear\s(\w*)$", cleaned_q)

    if is_near_search:
        # If we have a valid "near" operation, treat it as an "and" initially:
        cleaned_q = cleaned_q.replace(" near ", " and ")
    try:
        # Load all paragraph data into RAM.
        # Limit search by title, if applicable.

        paragraphs = Paragraph.objects.all()      
        if titles:
            paragraphs = paragraphs.filter(chapter__title__in=titles)
        paragraph_values = paragraphs.values()

        # We could, alternatively, compile a __regex filter search,
        # but the syntax of __regex is database-backend dependent.
        # This is better because it runs regex search at the
        # python level.

        def understand(o, patterns=None):
            numkeys = len(o.keys())

            result_ids = []

            unary_func = [
                "word", "quotes"
            ]
            binary_func = {
                "or" : "union",
                "and": "intersection",
            }

            def _django_query(o,operator,patterns=None):
                if operator == "word":
                    matchme = o[0]
                elif operator == "quotes":
                    elements = o.asList()
                    matchme = " ".join(flatten(elements))

                matchme = matchme.lower()
                matchme = make_wildcards_regex(matchme)
                pattern = "\\b" + matchme + "\\b"
                if patterns != None:
                    patterns.append(pattern)

                for paragraph in paragraph_values:
                    if re.search(pattern, paragraph['text'], re.IGNORECASE):
                        result_ids.append(paragraph['id'])
                result = set(result_ids)
                return result

            if numkeys == 0 and o.asDict() == {}:
                operator = o.getName()
                return _django_query(o,operator,patterns)
            elif numkeys == 1:
                #initial run.
                operator = o.keys().pop().lower()

                next = o[operator]

                if operator in binary_func:
                    next1, next2 = next
                    set1 = understand(next1, patterns)
                    set2 = understand(next2, patterns)
                    result = getattr(set1,binary_func[operator])(set2)
                    return result
                elif operator in unary_func:
                    return _django_query(next,operator,patterns)
                else:
                    raise InvalidSearchStringError("Unknown operator %s" % operator)
            else:
                raise InvalidSearchStringError("Something went wrong with keys in pyparsing search.")

        highlight_words = []
        id_matches = understand(parse(cleaned_q), highlight_words)

        if is_near_search:
            # If we have a valid "near" operation, see if is true.
            
            id_matches_old = list(id_matches)
            id_matches = []
            
            for paragraph in paragraph_values:
                if paragraph['id'] in id_matches_old:
                    words = re.findall(r"\b([A-Za-z0-9]+)\b", paragraph.text)
                    near1, near2 = is_near_search[0]
                
                    near1count = words.count(near1)
                    near2count = words.count(near2)

                    for i in range(len(words)):
                        if near1 == words[i]:
                            import pdb
                            pdb.set_trace()
                            for j in range(1,near_by_words+1):
                                if i+j < len(words) and near2 == words[i+j]:
                                    id_matches.append(paragraph['id'])
                                if i-j >= 0 and near2 == words[i-j]:
                                    id_matches.append(paragraph['id'])

            id_matches = set(id_matches)
            
        results_by_title = dict()

        title_ids_in_paragraphs = dict(paragraphs.values_list('id','page__title'))
        titles_by_id = dict([(title.id, title) for title in Title.objects.all()])

        num_results = 0
        for paragraph in paragraphs:
            title = titles_by_id[title_ids_in_paragraphs[paragraph.id]]
            if paragraph.id in id_matches:
                if not title in results_by_title:
                    results_by_title[title] = []
                results_by_title[title].append(paragraph)
                num_results += 1
        results_by_title = results_by_title.items()

    except InvalidSearchStringError:
        results_by_title = []
        num_results = 0

    return results_by_title, num_results, highlight_words


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
    ("*","wildcard","[A-Za-z0-9]*"),
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
		#print "Searching paragraph %s" % p.pk
		words.extend(p.get_words_for(word1))
		#print " found %s in paragraph %s" % (word1, p.pk)

	result = []
	
	for result_word1 in words:
		for nearby in result_word1.get_nearby(distance=num_words):
			if unicode(nearby) == unicode(word2):
				#print "%s is near %s" % (nearby, result_word1)
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