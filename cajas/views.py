from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Caja
from django.utils import timezone
from entidades.models import Entidad
from .forms import CajaForm

@login_required
def asignar_caja(request, caja_id):
    caja = get_object_or_404(Caja, id=caja_id)

    caja.responsable = request.user
    caja.fecha_asignacion = timezone.now().date()
    caja.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'mensaje': 'Caja asignada correctamente'})
    else:
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
    cajas = Caja.objects.filter(responsable=request.user)
    return render(request, 'cajas/historial.html', {'cajas': cajas})

@login_required
def inicio(request):
    return render(request, 'inicio.html')
