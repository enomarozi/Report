from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.contrib import messages
from django.urls import reverse
from .forms import Scanning
from .models import OutputFiles
from .views_convert import *
import os
import hashlib

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
				saveFiles = OutputFiles(name=nama,date=now(),md5check=checksum_file(nama))
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
	if len(data['nmaprun']['hosthint']) <= 3:
		address = data['nmaprun']['host']['address']['@addr']
		result = ', '.join([data['nmaprun']['host']['ports']['port'][i]['@portid'] for i in range(len(data['nmaprun']['host']['ports']['port']))])
		dict_[address] = result

	else:
		result = {}
		for i in data['nmaprun']['host']:
			address = i['address']['@addr']
			if type(i['ports']['extraports']) == dict:
				if int(i['ports']['extraports']['@count']) <= 1000:
					result[i['ports']['extraports']['@state']] = i['ports']['extraports']['@count']
					if "port" in i['ports']:
						result["Open"] = ', '.join([i['ports']['port'][j]['@portid'] for j in range(len(i['ports']['port']))])
			elif type(i['ports']['extraports']) == list:
				open_ = i['ports']['port']['@portid']
				for j in range(len(i['ports']['extraports'])):
					result[i['ports']['extraports'][j]['@state']] = i['ports']['extraports'][j]['@count']
				
				result["Open"] = open_
			dict_[address] = result
			result = {}
	return render(request, 'analisa.html',{'analisa':dict_}) 

def deleteFile(request, param):
	name_file = OutputFiles.objects.get(id=param)
	delete_files = OutputFiles.objects.filter(id=param).delete()
	ex_ = os.system(f"rm outputs/{name_file.name}")
	result = f'Delete File {name_file.name} is Successfully!'
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

def syncron(request):
	for i in os.listdir("outputs"):
		checksum_file(i)
	message = "Syncronfile Selesai"
	messages.success(request, message)
	return redirect('index')

def checksum_file(file):
	md5hash = hashlib.md5()
	with open("outputs/"+file,"rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			md5hash.update(chunk)
	if OutputFiles.objects.filter(md5check=md5hash.hexdigest()).exists():
		pass
	else:
		saveFiles = OutputFiles(name=file,date=now(),md5check=md5hash.hexdigest())
		saveFiles.save()

def data_result(request):
	files = os.listdir('outputs')
	result = []
	extension_allow = ["xml","html","json","null"]
	output_files = OutputFiles.objects.all().order_by("-date").values("id","name")
	for file in output_files:
		print(file)
		if len(file['name'].split('.')) == 2:
			file_name, file_extension = file['name'].split('.')
		else:
			file_name, file_extension = [file['name'],"null"]
		if file_extension in extension_allow:
			result.append({
				'name':file_name,
				'extension':file_extension,
				'id':file['id']
			}) 
	return JsonResponse(result, safe=False)




		
