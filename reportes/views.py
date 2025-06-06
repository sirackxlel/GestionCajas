from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cajas.models import Caja
from entidades.models import Entidad, Proceso
from django.http import HttpResponse
import pandas as pd
from django.utils.dateparse import parse_date

@login_required
def generar_reporte_excel(request):
    cajas = Caja.objects.select_related('entidad__proceso', 'responsable').all()

    # Filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    entidad_id = request.GET.get('entidad')
    estado = request.GET.get('estado')
    usuario_id = request.GET.get('usuario')

    if fecha_inicio:
        cajas = cajas.filter(fecha_asignacion__gte=parse_date(fecha_inicio))
    if fecha_fin:
        cajas = cajas.filter(fecha_asignacion__lte=parse_date(fecha_fin))
    if entidad_id:
        cajas = cajas.filter(entidad_id=entidad_id)
    if estado:
        cajas = cajas.filter(entidad__proceso__estado=estado)
    if usuario_id:
        cajas = cajas.filter(responsable_id=usuario_id)

    # Generar Excel
    data = []
    for c in cajas:
        data.append({
            'Número': c.numero,
            'Entidad': c.entidad.nombre if c.entidad else '',
            'Proceso': c.entidad.proceso.nombre if c.entidad and c.entidad.proceso else '',
            'Estado': c.entidad.proceso.estado if c.entidad and c.entidad.proceso else '',
            'Responsable': c.responsable.username if c.responsable else '',
            'Fecha Asignación': c.fecha_asignacion
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporte_cajas.xlsx"'
    df.to_excel(response, index=False)
    return response

@login_required
def formulario_reporte(request):
    entidades = Entidad.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'reportes/reporte.html', {
        'entidades': entidades,
        'usuarios': usuarios
    })