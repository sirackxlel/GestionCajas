from django.contrib import admin
from .models import Proceso, Entidad
# Register your models here.
@admin.register(Proceso)
class ProcesoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    search_fields = ('nombre', 'estado')

@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'proceso')
    search_fields = ('nombre',)
    list_filter = ('proceso',)