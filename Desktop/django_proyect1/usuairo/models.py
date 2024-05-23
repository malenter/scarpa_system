from django.db import models
from django.contrib.auth.models import User 
from .choices import TIPO_ZAPATO_CHOICES,ESTADO_DE_COMPRA
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='images/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    nombre_empresa = models.CharField(max_length=100,default='nombre')
    # Otros campos que desees agregar

    def __str__(self):
        return self.user.username
    

class Departamento(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name 


class Ciudad(models.Model):
    name = models.CharField(max_length=255)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    def __str__(self):
        return self.name 

class cliente (models.Model):
    nombre=models.CharField(max_length=100)
    correo=models.EmailField(max_length=254)
    numero=models.IntegerField()
    dirreccion=models.CharField( max_length=150)
    departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)
    ciudad =models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    local =models.CharField(max_length=100)

    def __str__(self):
      return f"{self.nombre} by {self.user.username}"

class Zapato (models.Model):
    nombre=models.CharField(max_length=100)
    color=models.CharField(max_length=50)
    tipo = models.CharField(max_length=50, choices=TIPO_ZAPATO_CHOICES)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    foto= models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
     return self.nombre + ' -by ' + self.user.username

class Factura (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(cliente , on_delete=models.CASCADE)
    fecha_pedido=models.DateField()
    pago =  models.BooleanField(default=False)
    fecha_de_entrega=models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nombre=models.CharField(max_length=60,default='Orden-#')

    def calcular_total(self):
        total_pedido = sum(pedido.valor for pedido in self.pedidos.all())
        self.total = total_pedido
        self.save()


    def __str__(self):
     return self.nombre + ' -by ' + self.user.username 

class Pedido (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zapato = models.ForeignKey(Zapato , on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura , on_delete=models.CASCADE,related_name='pedidos')
    estado = models.CharField(max_length=50, choices=ESTADO_DE_COMPRA ,default='no iniciado')
    canitdad=models.IntegerField(default=0)
    talla = models.CharField(max_length=60,default='tallas:')
    valor=models.IntegerField(default=0)
    fecha_pedido = models.DateField(default=timezone.now)


    def __str__(self):
      return self.zapato.nombre + ' -by ' + self.user.username
    def save(self, *args, **kwargs):
        # Recalcula el total de la factura cuando se guarda un pedido
        self.factura.calcular_total()
        super().save(*args, **kwargs)

class Encuesta (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(cliente , on_delete=models.CASCADE)
    pregunta_1 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    pregunta_2 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    pregunta_3 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    pregunta_4 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    pregunta_5 = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    pregunta_6 = models.TextField(default='recomendaciones:')




# Create your models here.
