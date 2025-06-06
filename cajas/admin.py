from django.contrib import admin
from .models import Caja

# Register your models here.
@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'entidad', 'responsable', 'fecha_asignacion')
    search_fields = ('numero',)
    list_filter = ('entidad', 'responsable')