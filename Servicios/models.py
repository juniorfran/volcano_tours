from django.db import models

# Create your models here.

class Camping(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad_personas = models.PositiveIntegerField()
    costo_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    tienda_camping = models.BooleanField()
    derecho_camping = models.DecimalField(max_digits=5, decimal_places=2)
    costo_parqueo = models.DecimalField( max_digits=5, decimal_places=2)
    horas_parqueo = models.DecimalField( max_digits=5, decimal_places=2)
    

    def __str__(self):
        return self.nombre
    
#modelo reserva
class ReservaCamping (models.Model):
    camping = models.ForeignKey(Camping, on_delete=models.PROTECT)  #Si se borra el camping, se elimin
    #tambien la reserva de este campi
    fecha_inicio = models.DateField('Fecha Inicio')
    fecha_fin = models.DateField('Fecha Fin')
   
        

class AlquilerCabanias(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    capacidad_personas = models.PositiveIntegerField()
    costo_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    comodidades = models.TextField()

    def __str__(self):
        return self.nombre

