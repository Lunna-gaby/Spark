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
    path('direcao/', views.area_direcao, name='area_direcao'),
    path('direcao/reservas/', views.direcao_reservas, name='direcao_reservas'),
    path('direcao/reservas/aprovar/<int:id>/', views.aprovar_reserva, name='aprovar_reserva'),
    path('direcao/reservas/recusar/<int:id>/', views.recusar_reserva, name='recusar_reserva'),
    path(
    'direcao/reservas/excluir/<int:id>/',
    views.excluir_reserva_direcao,
    name='excluir_reserva_direcao'
),
path(
    'direcao/equipamentos/',
    views.direcao_equipamentos,
    name='direcao_equipamentos'
),
path(
    'direcao/usuarios/',
    views.direcao_usuarios,
    name='direcao_usuarios'
),
path(
    'direcao/usuarios/excluir/<int:id>/',
    views.excluir_usuario_direcao,
    name='excluir_usuario_direcao'
),
]