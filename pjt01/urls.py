"""config URL Configuration

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
from django.urls import path
from pjt01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('c1', views.c1, name='c1'),
    path('c1data', views.c1data, name='c1data'),
    path('iots', views.iots, name='iots'),
    path('img', views.img, name='img'),
    path('map', views.map, name='map'),

    path('chart1', views.chart1, name='chart1'),
    path('chart2', views.chart2, name='chart2'),
    path('chart3', views.chart3, name='chart3'),
    path('chart4', views.chart4, name='chart4'),

    path('chart1s', views.chart1s, name='chart1s'),
    path('chart2s', views.chart2s, name='chart2s'),
    path('chart3s', views.chart3s, name='chart3s'),
    path('chart4s', views.chart4s, name='chart4s'),

    path('test', views.test, name='test'),

]
