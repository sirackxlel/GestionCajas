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
from django.db.models import Count, Q

@login_required
def asignar_caja(request):
    # Obtener entidad activa o activarla si no existe
    entidad = Entidad.objects.filter(activa=True).first()
    caja = None

    if not entidad or not Caja.objects.filter(entidad=entidad, responsable__isnull=True).exists():
        if entidad:
            entidad.activa = False
            entidad.save()

        entidad = (
            Entidad.objects
            .annotate(cajas_libres=Count('caja', filter=Q(caja__responsable__isnull=True)))
            .filter(cajas_libres__gt=0)
            .order_by('-cajas_libres')
            .first()
        )
    if not entidad:
        entidad = Entidad.objects.filter(caja__responsable__isnull=True).order_by('?').first()
        if entidad:
            entidad.activa = True
            entidad.save()

    if entidad:
        caja = Caja.objects.filter(entidad=entidad, responsable__isnull=True).first()

    if not caja:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'mensaje': 'No hay cajas disponibles'})
        messages.error(request, 'No hay cajas disponibles')
        return redirect('lista_cajas')
    
    hoy = timezone.now().date()
    # Marcar como finalizadas las cajas activas del usuario
    Caja.objects.filter(responsable=request.user, fecha_finalizacion__isnull=True).update(fecha_finalizacion=hoy)

    caja.responsable = request.user
    caja.fecha_asignacion = hoy
    caja.fecha_finalizacion = None
    caja.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'ok': True,
            'mensaje': f'Caja asignada correctamente: Caja #{caja.numero}'  # <-- mostrar número o id
        })
    messages.success(request, 'Caja asignada correctamente')
    return redirect('historial')
    
@login_required
def crear_caja(request):
    entidad_seleccionada = None

    if request.method == 'POST':
        numero = request.POST['numero']
        entidad_id = request.POST['entidad']
        entidad = get_object_or_404(Entidad, id=entidad_id)

        # Verificar si ya existe una caja con ese número
        if Caja.objects.filter(numero=numero).exists():
            messages.error(request, f"Ya existe una caja con el número {numero}.")
        else:
            try:
                Caja.objects.create(numero=numero, entidad=entidad)
                messages.success(request, f"Caja número {numero} creada exitosamente.")
                return redirect('crear_caja')  # 🔄 Redirecciona para evitar reenvío del formulario
            except Exception as e:
                messages.error(request, f"Error al crear la caja: {str(e)}")

        entidad_seleccionada = int(entidad_id)  # ✅ Retener selección del usuario

    entidades = Entidad.objects.all()
    return render(request, 'cajas/crear.html', {
        'entidades': entidades,
        'entidad_seleccionada': entidad_seleccionada
    })

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
    total_cajas = Caja.objects.count()
    total_cajas_abiertas = Caja.objects.filter(fecha_finalizacion__isnull=True).count()  # ✅ Solo abiertas
    entidad_activa = Entidad.objects.filter(activa=True).first()

    if entidad_activa:
        cajas_entidad_activa = Caja.objects.filter(
            entidad=entidad_activa,
            fecha_finalizacion__isnull=True,
        ).count()
        cajas_proceso = Caja.objects.filter(
            entidad__proceso=entidad_activa.proceso,
            fecha_finalizacion__isnull=True,
        ).count()
    else:
        cajas_entidad_activa = 0
        cajas_proceso = 0

    ultima_caja = (
        Caja.objects.filter(responsable=request.user)
        .order_by('-fecha_asignacion')
        .first()
    )

    context = {
        'total_cajas': total_cajas,
        'total_cajas_abiertas': total_cajas_abiertas,
        'entidad_activa': entidad_activa,
        'cajas_entidad_activa': cajas_entidad_activa,
        'cajas_proceso': cajas_proceso,
        'ultima_caja': ultima_caja,
    }
    return render(request, 'inicio.html', context)
