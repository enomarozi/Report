from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('scanner/', views.scanner, name='scanner'),
	path('convertFile/<str:param>/', views.convertFile, name='convertFile'),
	path('openFile/<str:param>/', views.openFile, name='openFile'),
	path('analisaFile/<str:param>/', views.analisaFile, name='analisaFile'),
<<<<<<< HEAD
	path('deleteFile/<str:param>/', views.deleteFile, name='deleteFile'),
=======
	path('deleteFile/<int:param>/', views.deleteFile, name='deleteFile'),
>>>>>>> 159bc4dbd8d99be2d510890f7290ac9b4c3be034
	path('data_result/', views.data_result, name='data_result'),

]