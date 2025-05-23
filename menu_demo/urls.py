"""menu_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path


def index(request):
    return render(request, 'base.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='base'),
    path('catalog/', index, name='cat'),
    path('catalog/bytovaya-tehnika', index),
    path('catalog/smartfony-i-telefony', index),
    path('catalog/smartfony-i-telefony/smart', index),
    path('catalog/bytovaya-tehnika/holodolniki', index),
    path('catalog/bytovaya-tehnika/elektrochajniki', index, name='elektrochajniki'),
    path('catalog/pk_noutbuki', index),
    path('catalog/instrumenti', index),
    path('about/', index),
    path('contacts/', index),
]

