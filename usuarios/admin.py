from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'nombre', 'apellido', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Datos personales', {'fields': ('nombre', 'apellido')}),
    )