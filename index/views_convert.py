from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from .models import OutputFiles
from lxml import etree
import xmltodict
import json
import os
import hashlib

def xml_to_html(file_path, xslt_file):
	xml_tree = etree.parse(file_path)
	xslt_tree = etree.parse(xslt_file)
	transform = etree.XSLT(xslt_tree)
	html_tree = transform(xml_tree)

	filename = file_path.replace("xml","html")
	nama = filename.split("outputs/")[1].replace(' ','')
	with open(filename, "wb") as f:
		f.write(etree.tostring(html_tree, pretty_print=True))
	checksum_file(nama)

def xml_to_json(file_path):
	with open(file_path,"r") as xml_file:
		xml_string = xml_file.read()

	xml_dict = xmltodict.parse(xml_string)
	json_string = json.dumps(xml_dict, indent=4)
	filename = file_path.replace("xml","json")
	nama = filename.split("outputs/")[1].replace(' ','')
	with open(filename, "w") as f:
		f.write(json_string)
	checksum_file(nama)

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