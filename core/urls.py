from django.urls import path
from . import views

urlpatterns = [
    path('',       views.home,  name='home'),
    path('about/', views.about, name='about'),
    path('tracks/', views.tracks, name='tracks'),
    path('tracks/<slug:slug>/', views.domain_detail, name='domain_detail'),
]
