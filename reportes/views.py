from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cajas.models import Caja
from entidades.models import Entidad, Proceso
from django.http import HttpResponse
import pandas as pd
from django.utils.dateparse import parse_date
from usuarios.models import Usuario
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import io
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
def generar_reporte_pdf(request):
    """Genera un reporte en formato PDF filtrado por tipo y proceso."""
    cajas = Caja.objects.select_related("entidad__proceso", "responsable").all()

    tipo = request.GET.get("tipo", "mensual")
    mes = request.GET.get("mes")
    year = request.GET.get("year")
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    proceso_id = request.GET.get("proceso")

    if tipo == "mensual" and mes:
        try:
            y, m = mes.split("-")
            cajas = cajas.filter(
                fecha_asignacion__year=int(y),
                fecha_asignacion__month=int(m),
            )
        except ValueError:
            pass
    elif tipo == "anual" and year:
        try:
            cajas = cajas.filter(fecha_asignacion__year=int(year))
        except ValueError:
            pass
    elif tipo == "personalizado":
        if fecha_inicio:
            cajas = cajas.filter(fecha_asignacion__gte=parse_date(fecha_inicio))
        if fecha_fin:
            cajas = cajas.filter(fecha_asignacion__lte=parse_date(fecha_fin))

    if mes:
        try:
            year, month = mes.split('-')
            cajas = cajas.filter(
                fecha_asignacion__year=int(year),
                fecha_asignacion__month=int(month),
            )
        except ValueError:
            pass

    if proceso_id:
        cajas = cajas.filter(entidad__proceso_id=proceso_id)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = [Paragraph('Reporte de Cajas', styles['Heading1'])]

    data = [['Número', 'Entidad', 'Proceso', 'Responsable', 'Fecha Asignación']]
    for c in cajas:
        data.append([
            c.numero,
            c.entidad.nombre if c.entidad else '',
            c.entidad.proceso.nombre if c.entidad else '',
            c.responsable.username if c.responsable else '',
            c.fecha_asignacion.strftime('%Y-%m-%d') if c.fecha_asignacion else '',
        ])

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )
    )
    elements.append(table)
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_cajas.pdf"'
    return response

@login_required
def formulario_reporte(request):
    entidades = Entidad.objects.all()
    usuarios = Usuario.objects.all()
    procesos = Proceso.objects.all()
    return render(
        request,
        'reportes/reporte.html',
        {
            'entidades': entidades,
            'usuarios': usuarios,
            'procesos': procesos,
        },
    )