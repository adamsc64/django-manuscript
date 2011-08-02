from manuscript.models import compile_paragraphs
from django.http import HttpResponse

def recreate_paragraph_composites(request):
	compile_paragraphs(flush=True)
	return HttpResponse("Seems to have run ok.")