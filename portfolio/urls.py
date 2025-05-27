"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from resume import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resume.urls')), # this is the main url for the resume app
    path('resume/', views.resume, name='resume'), # this is the url for the resume page and the views.resume function
    path('resume/generate-pdf/', views.generate_pdf, name='generate_pdf'), # this is the url for the generate pdf page and the views.generate_pdf function
]
