from django import forms
from entidades.models import Entidad, Proceso
from usuarios.models import Usuario

class FiltroReporteForm(forms.Form):
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    entidad = forms.ModelChoiceField(queryset=Entidad.objects.all(), required=False)
    estado = forms.ChoiceField(choices=[('', '---------'), ('pendiente', 'Pendiente'), ('en_curso', 'En Curso'), ('finalizado', 'Finalizado')], required=False)
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), required=False)
