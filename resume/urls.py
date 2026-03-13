from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blogs/<slug:slug>/comment/', views.blog_comment_create, name='blog_comment_create'),
    path('downloads/', views.download_list, name='download_list'),
    path('downloads/bulk/', views.download_bulk, name='download_bulk'),
    path('downloads/<slug:slug>/', views.download_detail, name='download_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('resume/', views.resume, name='resume'),
    path('resume/preview/', views.resume_preview, name='resume_preview'),
    path('resume/generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('about/', RedirectView.as_view(url='/#about', permanent=False)),
    path('projects/', RedirectView.as_view(url='/#projects', permanent=False)),
    path('skills/', RedirectView.as_view(url='/#skills', permanent=False)),
    path('education/', RedirectView.as_view(url='/#education', permanent=False)),
    path('experience/', RedirectView.as_view(url='/#experience', permanent=False)),
    path('certifications/', RedirectView.as_view(url='/#certifications', permanent=False)),
]

