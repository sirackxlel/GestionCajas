from django.shortcuts import render, redirect, get_object_or_404
from .models import Entidad, Proceso
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# CREAR
@login_required
def crear_entidad(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        proceso_id = request.POST['proceso']
        proceso = get_object_or_404(Proceso, id=proceso_id)
        Entidad.objects.create(nombre=nombre, proceso=proceso)
        return redirect('lista_entidades')
    procesos = Proceso.objects.all()
    return render(request, 'entidades/crear_entidad.html', {'procesos': procesos})

# LISTAR
@login_required
def lista_entidades(request):
    entidades = Entidad.objects.all()
    return render(request, 'entidades/lista_entidades.html', {'entidades': entidades})

# ACTUALIZAR
@login_required
def editar_entidad(request, entidad_id):
    entidad = get_object_or_404(Entidad, id=entidad_id)
    if request.method == 'POST':
        entidad.nombre = request.POST['nombre']
        entidad.proceso_id = request.POST['proceso']
        entidad.save()
        return redirect('lista_entidades')
    procesos = Proceso.objects.all()
    return render(request, 'entidades/editar_entidad.html', {'entidad': entidad, 'procesos': procesos})

@login_required
@user_passes_test(lambda u: u.is_staff)
def priorizar_entidad(request, entidad_id):
    entidad = get_object_or_404(Entidad, id=entidad_id)
    Entidad.objects.update(activa=False)
    entidad.activa = True
    entidad.save() 
    proceso = entidad.proceso
    if proceso.estado == "pendiente":
        proceso.estado = "en_curso"
        proceso.save()
    messages.success(request, 'Entidad priorizada correctamente')
    return redirect('lista_entidades')


# ELIMINAR
@login_required
def eliminar_entidad(request, entidad_id):
    entidad = get_object_or_404(Entidad, id=entidad_id)
    entidad.delete()
    return redirect('lista_entidades')

# CREAR
@login_required
def crear_proceso(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        estado = request.POST['estado']
        proceso = Proceso.objects.create(nombre=nombre, estado=estado)
        entidades = [Entidad(nombre=str(i), proceso=proceso) for i in range(1, 301)]
        Entidad.objects.bulk_create(entidades)
        return redirect('lista_procesos')
        return redirect('lista_procesos')
    return render(request, 'procesos/crear_proceso.html')

# LISTAR
@login_required
def lista_procesos(request):
    procesos = Proceso.objects.all()
    return render(request, 'procesos/lista_procesos.html', {'procesos': procesos})

# ACTUALIZAR
@login_required
def editar_proceso(request, proceso_id):
    proceso = get_object_or_404(Proceso, id=proceso_id)
    if request.method == 'POST':
        proceso.nombre = request.POST['nombre']
        proceso.estado = request.POST['estado']
        proceso.save()
        return redirect('lista_procesos')
    return render(request, 'entidades/editar_proceso.html', {'proceso': proceso})

# ELIMINAR
@login_required
def eliminar_proceso(request, proceso_id):
    proceso = get_object_or_404(Proceso, id=proceso_id)
    proceso.delete()
    return redirect('lista_procesos')
    
@login_required
def cambiar_estado_proceso(request, proceso_id):
    """Actualizar el estado de un proceso desde la lista."""
    proceso = get_object_or_404(Proceso, id=proceso_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado:
            if nuevo_estado == "en_curso":
                # Solo puede haber un proceso en curso a la vez
                (Proceso.objects
                        .filter(estado="en_curso")
                        .exclude(id=proceso_id)
                        .update(estado="pendiente"))
            proceso.estado = nuevo_estado
            proceso.save()
    return redirect('lista_procesos')
