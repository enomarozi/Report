from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request, 'index.html')
def index1(request):
	# context = {
	# 	"title":"Dashboard",
	# }
	# return render(request, 'index/index.html', context)
	return HttpResponse("<h1>ENO MAROZI</h1>")