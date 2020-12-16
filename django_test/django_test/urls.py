"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.contrib.auth import login
from UserLogin import views as v

handler404 = 'catalog.views.error_404'

urlpatterns = [
    path('' , include('UserLogin.urls')),
    path('admin/', admin.site.urls),
    path('register/',v.register,name='register'),
    url('' , include('django.contrib.auth.urls')),
    path('catalog/' , include('catalog.urls')),
    #path('addpoint/', views.addpoints, name='user-addpoint'),
    #path('PostPoint/', views.PostPoint, name='user-postpoint'),
]