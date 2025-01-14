from django.shortcuts import render

def index(request):
	context = {
		"title":"Dashboard",
	}
	return render(request, 'index/index.html', context)
