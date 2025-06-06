from django.urls import path
from . import views

urlpatterns = [
    # ENTIDADES
    path('entidades/', views.lista_entidades, name='lista_entidades'),
    path('entidades/crear/', views.crear_entidad, name='crear_entidad'),
    path('entidades/editar/<int:entidad_id>/', views.editar_entidad, name='editar_entidad'),
    path('entidades/eliminar/<int:entidad_id>/', views.eliminar_entidad, name='eliminar_entidad'),

    # PROCESOS
    path('procesos/', views.lista_procesos, name='lista_procesos'),
    path('procesos/crear/', views.crear_proceso, name='crear_proceso'),
    path('procesos/editar/<int:proceso_id>/', views.editar_proceso, name='editar_proceso'),
    path('procesos/eliminar/<int:proceso_id>/', views.eliminar_proceso, name='eliminar_proceso'),
]
