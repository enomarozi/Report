from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .forms import Scanning
from django.contrib import messages
from django.urls import reverse
import os, re

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

def openFile(request, param):
	type_ = param.split('.') 
	file_path = os.path.join('outputs',param)
	if os.path.exists(file_path):
		with open(file_path, 'r') as file:
			file_content = file.read()

		if type_[1] == "html":
			return HttpResponse(file_content, content_type='text/html')
		elif type_[1] == "xml":
			return HttpResponse(file_content, content_type='application/xml')
		elif type_[1] == "json":
			return HttpResponse(file_content, content_type='application/json')
	else:
		return HttpResponse("File not found.",status=404)

def convertFile(request, param):
	print(param)

def deleteFile(request, param):
	ex_ = os.system("rm outputs/"+param)
	if ex_ == 0:
		result = f'Delete File {param} is Successfully!'
	messages.success(request, result)
	return HttpResponseRedirect(reverse('index'))

def data_result(request):
	files = os.listdir('outputs')
	result = []
	extension_allow = ["xml","html","json"]
	for file in files:
		file_name, file_extension = file.split('.')
		if file_extension in extension_allow:
			result.append({
				'name':file_name,
				'extension':file_extension,
			}) 
	return JsonResponse(result, safe=False)




		
