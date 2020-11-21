from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('convalidation/', views.convalidation, name='convalidation'),
    path('applypair/', views.applypair, name='applypair'),
    path('confirmar_pareja/', views.confirmar_pareja, name='confirmar_pareja'),
    path('elegir_grupo/', views.elegir_grupo, name='elegir_grupo'),
    path('confirmar_grupo/', views.confirmar_grupo, name='confirmar_grupo'),
]