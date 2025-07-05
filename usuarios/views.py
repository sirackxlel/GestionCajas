from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')  # redirigir aquí
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro_usuario.html', {'form': form})

Usuario = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_staff)
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if usuario != request.user:  # evitar que se elimine a sí mismo
        usuario.delete()
    return redirect('listar_usuarios')
