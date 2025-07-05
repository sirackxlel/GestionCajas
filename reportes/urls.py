from django.urls import path
from . import views

urlpatterns = [
    path('excel/', views.generar_reporte_excel, name='reporte_excel'),
    path('pdf/', views.generar_reporte_pdf, name='reporte_pdf'),
    path('', views.formulario_reporte, name='formulario_reporte'),
]
