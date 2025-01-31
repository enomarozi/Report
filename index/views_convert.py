from django.shortcuts import render
from django.utils.timezone import now
from .models import OutputFiles
from lxml import etree
import xmltodict
import json

def xml_to_html(file_path, xslt_file):
	xml_tree = etree.parse(file_path)
	xslt_tree = etree.parse(xslt_file)
	transform = etree.XSLT(xslt_tree)
	html_tree = transform(xml_tree)

	filename = file_path.replace("xml","html")
	saveFiles = OutputFiles(name=filename,date=now())
	saveFiles.save()
	with open(filename, "wb") as f:
		f.write(etree.tostring(html_tree, pretty_print=True))

def xml_to_json(file_path):
	with open(file_path,"r") as xml_file:
		xml_string = xml_file.read()

	xml_dict = xmltodict.parse(xml_string)
	json_string = json.dumps(xml_dict, indent=4)
	filename = file_path.replace("xml","json")
	saveFiles = OutputFiles(name=filename,date=now())
	saveFiles.save()
	with open(filename, "w") as f:
		f.write(json_string)
