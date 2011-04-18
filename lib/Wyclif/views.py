from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound

#def googleproof(request):
#	return HttpResponse('google-site-verification: googled05e050f361f6ab1.html')

def robotstxt(request):
	return HttpResponse("User-agent: *\r\nDisallow: /\r\n")
	
def do404(request):
	#raise Http404()
	#return HttpResponseNotFound()
	return HttpResponseRedirect('/')

def index(request):
	return render_to_response('Wyclif/index.html')