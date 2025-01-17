from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import Scanning
import os

def index(request):
	form = Scanning()
	return render(request,"index.html",{'form':form})

def scanner(request):
	if request.method == "GET":
		form = Scanning(data=request.GET)
		if form.is_valid():
			command = form.cleaned_data.get('command')
			os.system(command)
			return HttpResponse(f"Command received: {command}")
		else:
			return HttpResponse(f"Invalid from data",status=400)

	return HttpResponse("Method not allowed", status=405)

def data_result(request):
	files = os.listdir('outputs')
	result = []
	for file in files:
		file_name, file_extension = os.path.splitext(file)
		result.append({
			'name':file_name,
			'extension':file_extension[1:],
			}) 
	return JsonResponse(result, safe=False)



		
