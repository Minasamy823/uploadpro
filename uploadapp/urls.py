from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', imagesList, name='image_list'),
    path('upload/', uploading, name='uploading'),
    re_path(r'(?P<hash>\w+)/$', ChangeImage, name='image_detail'),
]