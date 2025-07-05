from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Caja
from django.utils import timezone
from entidades.models import Entidad
from .forms import CajaForm
from usuarios.models import Usuario
from django.contrib import messages

@login_required
def asignar_caja(request):
    # Obtener entidad activa o activarla si no existe
    entidad = Entidad.objects.filter(activa=True).first()

    if not entidad:
        entidad = Entidad.objects.filter(caja__responsable__isnull=True).order_by('?').first()
        if entidad:
            entidad.activa = True
            entidad.save()

    if entidad:
        caja = Caja.objects.filter(entidad=entidad, responsable__isnull=True).order_by('?').first()
        if not caja:
            # No hay cajas libres en la entidad activa -> desactivarla y buscar otra
            entidad.activa = False
            entidad.save()
            nueva_entidad = Entidad.objects.filter(caja__responsable__isnull=True).order_by('?').first()
            if nueva_entidad:
                nueva_entidad.activa = True
                nueva_entidad.save()
                caja = Caja.objects.filter(entidad=nueva_entidad, responsable__isnull=True).order_by('?').first()
    else:
        caja = None

    if not caja:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'mensaje': 'No hay cajas disponibles'})
        messages.error(request, 'No hay cajas disponibles')
        return redirect('lista_cajas')

    caja.responsable = request.user
    caja.fecha_asignacion = timezone.now().date()
    caja.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'mensaje': 'Caja asignada correctamente'})
    messages.success(request, 'Caja asignada correctamente')
    return redirect('historial')
@login_required
def crear_caja(request):
    if request.method == 'POST':
        numero = request.POST['numero']
        entidad_id = request.POST['entidad']
        entidad = get_object_or_404(Entidad, id=entidad_id)
        Caja.objects.create(numero=numero, entidad=entidad)
        return redirect('lista_cajas')  
    entidades = Entidad.objects.all()
    return render(request, 'cajas/crear.html', {'entidades': entidades})

@login_required
def lista_cajas(request):
    cajas = Caja.objects.all()
    return render(request, 'cajas/lista.html', {'cajas': cajas})

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_caja(request, caja_id):
    caja = get_object_or_404(Caja, id=caja_id)
    if request.method == 'POST':
        form = CajaForm(request.POST, instance=caja)
        if form.is_valid():
            form.save()
            return redirect('lista_cajas')
    else:
        form = CajaForm(instance=caja)
    return render(request, 'cajas/editar_caja.html', {'form': form})

@login_required
def eliminar_caja(request, caja_id):
    caja = get_object_or_404(Caja, id=caja_id)
    caja.delete()
    return redirect('lista_cajas')

@login_required
def historial(request):
    """Muestra el historial de cajas asignadas."""
    if request.user.is_staff:
        User = Usuario
        usuarios = User.objects.all()
        cajas_por_usuario = {
            usuario: Caja.objects.filter(responsable=usuario)
            .order_by('-fecha_asignacion')
            for usuario in usuarios
        }
        context = {
            'admin_view': True,
            'cajas_por_usuario': cajas_por_usuario,
        }
    else:
        cajas = Caja.objects.filter(responsable=request.user).order_by('-fecha_asignacion')
        context = {
            'admin_view': False,
            'cajas': cajas,
        }
    return render(request, 'cajas/historial.html', context)

@login_required
def inicio(request):
    return render(request, 'inicio.html')
