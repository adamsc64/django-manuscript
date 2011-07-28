import re

def flatten(l):
	out = []
	for item in l:
		if isinstance(item, (list, tuple)):
		  	out.extend(flatten(item))
		else:
		  	out.append(item)
	return out

def _full_word_regex(word):
	return r"\b%s\b" % word

def convert_to_regex_search(expr):
	expr = expr.replace("(","~")
	expr = expr.replace(")","%")
	
	def __finder(expr):
		print "gets " + expr
		regex = re.compile(r"\~[^\(\)]+\%")
		match = regex.search(expr)
		if match:
			sub_expr = match.group()
			result = __finder(expr.replace(sub_expr, str(__finder(sub_expr[1:-1]))))
			print "results " + result
			return result
		result = _to_regex(expr)
		print "results" + result
		return result

	return __finder(expr)

def _to_regex(q):

	q = q.replace("*","\w*")
	ORs = q.split(" OR ")
	
	or_list = []
	
	for OR in ORs:
		ANDs = OR.split(" AND ")
		if len(ANDs) > 1:
			conditions = []
			for i in range(len(ANDs)):
				word1 = ANDs[i]
				for j in range(i,len(ANDs)):
					word2 = ANDs[j]
					if word1 != word2:
						conditions.append(_full_word_regex(word1 + ".*" + word2))
						conditions.append(_full_word_regex(word2 + ".*" + word1))
		else:
			conditions = [_full_word_regex(ANDs[0])]
				
		or_list.append("|".join("(%s)" % condition for condition in conditions))
		
		regex = ("(%s)" % "|".join(o for o in or_list)) if len(or_list)>1 else or_list[0]
	
	return regex