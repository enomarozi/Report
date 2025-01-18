from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('scanner/', views.scanner, name='scanner'),
	path('convertFile/<str:param>/', views.convertFile, name='convertFile'),
	path('openFile/<str:param>/', views.openFile, name='openFile'),
	path('deleteFile/<str:param>/', views.deleteFile, name='deleteFile'),
	path('data_result/', views.data_result, name='data_result'),

]