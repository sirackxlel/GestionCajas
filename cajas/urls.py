from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.lista_cajas, name='lista_cajas'),  # ← ESTA es la que falta
    path('asignar/', views.asignar_caja, name='asignar_caja'),
    path('crear/', views.crear_caja, name='crear_caja'),
    path('editar/<int:caja_id>/', views.editar_caja, name='editar_caja'),
    path('eliminar/<int:caja_id>/', views.eliminar_caja, name='eliminar_caja'),
    path('historial/', views.historial, name='historial'),
]
