from django.urls import path
from .views import registrar_usuario, listar_usuarios, eliminar_usuario

urlpatterns = [
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('listar/', listar_usuarios, name='listar_usuarios'),
    path('eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
]
