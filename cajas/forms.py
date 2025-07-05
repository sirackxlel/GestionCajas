from django import forms
from .models import Caja

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['numero', 'entidad', 'responsable', 'fecha_asignacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
