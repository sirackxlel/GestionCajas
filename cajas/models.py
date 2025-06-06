from datetime import timezone
from django.db import models
from entidades.models import Entidad, Proceso
from usuarios.models import Usuario
# Create your models here.
class Caja(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    entidad = models.ForeignKey(Entidad, on_delete=models.SET_NULL, null=True, blank=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_asignacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Caja #{self.numero}"
