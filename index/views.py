from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.contrib import messages
from django.urls import reverse
from .forms import Scanning
from .models import OutputFiles
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
				nama = command.split("outputs/")[1].replace(' ','')
				saveFiles = OutputFiles(name=nama,date=now())
				saveFiles.save()
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

def analisaFile(request, param):
	file_path = os.path.join('outputs',param)
	with open(file_path,'r') as file:
		data = json.load(file)
	dict_ = {}
	if "hosthint" in data["nmaprun"]:
		if len(data['nmaprun']['hosthint']) <= 3:
			address = data['nmaprun']['host']['address']['@addr']
			result = ', '.join([data['nmaprun']['host']['ports']['port'][i]['@portid'] for i in range(len(data['nmaprun']['host']['ports']['port']))])
			dict_[address] = result

		else:
			for i in data['nmaprun']['host']:
				address = i['address']['@addr']
				if "port" in i["ports"]:
					if type(i['ports']['port']) == dict:
						result = i['ports']['port']['@portid']
					elif type(i['ports']['port']) == list:
						result = ', '.join([i['ports']['port'][j]['@portid'] for j in range(len(i['ports']['port']))])
				else:
					result = "Down / No Port Active"
				dict_[address] = result
	return render(request, 'analisa.html',{'analisa':dict_}) 

def deleteFile(request, param):
	delete_files = OutputFiles.objects.filter(name=param).delete()
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
	output_files = OutputFiles.objects.all().order_by("-date").values("name")
	for file in output_files:
		file_name, file_extension = file['name'].split('.')
		if file_extension in extension_allow:
			result.append({
				'name':file_name,
				'extension':file_extension,
			}) 
	return JsonResponse(result, safe=False)




		
