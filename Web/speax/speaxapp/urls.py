from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.simple_upload, name='simple_upload'),    
]
