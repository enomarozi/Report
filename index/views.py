from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .forms import Scanning
from .views_convert import *
import os, re

def index(request):
	form = Scanning()
	return render(request,"index.html",{'form':form})

def scanner(request):
	form = Scanning(data=request.GET)
	if request.method == "GET":
		if form.is_valid():
			command = form.cleaned_data.get('command')
			if validation(command) == True:
				os.system(command)
				message = "Scanning Selesai"
			else:
				message = "Maaf, Command tidak dizinkan!!"
			messages.success(request, message)
			return redirect('index')
		else:
			return redirect('index')

	return render(request, 'index.html',{'form':form})

def openFile(request, param):
	type_ = param.split('.') 
	file_path = os.path.join('outputs',param)
	if os.path.exists(file_path):
		with open(file_path, 'r', encoding="utf-8") as file:
			file_content = file.read()

		if type_[1] == "html":
			return HttpResponse(file_content, content_type='text/html')
		elif type_[1] == "json":
			return HttpResponse(file_content, content_type='application/json')
	else:
		return HttpResponse("File not found.",status=404)

def convertFile(request, param):
	if os.name == "nt":
		xslt_file = "C:/Program Files (x86)/Nmap/nmap.xsl"
	elif os.name == "posix":
		xslt_file = "/usr/share/nmap/nmap.xsl"

	file_path = "outputs/"+param
	if os.path.exists(file_path):
		extention_html = xml_to_html(file_path, xslt_file)
		json = "outputs/"+param.replace("xml","json")
		extention_json = xml_to_json(file_path)

	messages.success(request, "Convert Selesai")
	return redirect('index')

def deleteFile(request, param):
	ex_ = os.system(f"rm outputs/{param}")
	if ex_ == 0:
		result = f'Delete File {param} is Successfully!'
	messages.success(request, result)
	return HttpResponseRedirect(reverse('index'))

def validation(command):
	array_block = ["|","&"]
	if "nmap" in command:
		for bl in array_block:
			if bl not in command:
				return True			
			else:
				return False
	else:
		return False

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




		
