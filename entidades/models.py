from django.db import models

# Create your models here.
class Proceso(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=[
        ("pendiente", "Pendiente"),
        ("en_curso", "En Curso"),
        ("finalizado", "Finalizado")
    ])

    def __str__(self):
        return f"{self.nombre} ({self.estado})"


class Entidad(models.Model):
    nombre = models.CharField(max_length=100)
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE)
    activa = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
