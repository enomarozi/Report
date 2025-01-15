from django.shortcuts import render
from django.http import HttpResponse
import os

def index(request):
	return render(request, 'index.html')

def scanner(request):
	if request.method == "POST":
		
