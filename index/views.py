from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import Scanning
from django.contrib import messages
import os

def index(request):
	form = Scanning()
	return render(request,"index.html",{'form':form})

def scanner(request):
	form = Scanning(data=request.GET)
	if request.method == "GET":
		if form.is_valid():
			command = form.cleaned_data.get('command')
			os.system(command)
			messages.success(request, "Scanning Selesai")
		else:
			return HttpResponse(f"Invalid from data",status=400)

	return render(request, 'index.html',{'form':form})

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



		
