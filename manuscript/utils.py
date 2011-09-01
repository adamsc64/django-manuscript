import re

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
