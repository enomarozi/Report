from django import forms
from django.core.validators import FileExtensionValidator

class Scanning(forms.Form):
	command = forms.CharField(label='Command', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Command'}))
