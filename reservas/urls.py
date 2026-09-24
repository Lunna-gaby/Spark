from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.fazer_login, name='login'),
    path('cadastro/', views.fazer_cadastro, name='cadastro'),
    path('equipamentos/', views.listar_equipamentos, name='equipamentos'),
    path('reservar/', views.fazer_reserva, name='fazer_reserva'),
    path('reservas-realizadas/', views.reservas_realizadas, name='reservas_realizadas'),
    path('excluir-reserva/<int:id>/', views.excluir_reserva, name='excluir_reserva'),
]