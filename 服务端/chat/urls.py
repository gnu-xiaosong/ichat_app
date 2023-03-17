# _*_ coding: utf-8 _*_

from django.contrib import admin
from django.urls import path
from .view import chatgpt,index, uploadFile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', chatgpt),
    path('index/', index),
    path('uploadFile/', uploadFile),
]
