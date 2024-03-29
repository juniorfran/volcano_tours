from django.conf import settings
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.core.mail import EmailMultiAlternatives
import qrcode
from io import BytesIO
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from Transacciones.models import EnlacePago

# Create your models here.

#modelos para tours
class TipoTour(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre
    
class Tour(models.Model):
    titulo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    descripcion1 = models.TextField()
    descripcion2 = models.TextField()
    precio_adulto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nino = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.PositiveIntegerField()
    iva = models.BooleanField(default=False)
    incluye_tour = models.TextField()
    
    imagen = models.ImageField(upload_to='tours')
    tipo_tour = models.ForeignKey(TipoTour, on_delete=models.SET_NULL, null=True, blank=True)

    def obtener_imagen_principal(self):
        return self.imagen.url

    def __str__(self):
        return f"{self.titulo} - ${self.precio_adulto}"

class ImagenTour(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='tours/%Y/%m/%d/')
    imagen1 = models.ImageField(upload_to='tours/%Y/%m/%d/')
    imagen2 = models.ImageField(upload_to='tours/%Y/%m/%d/')
    imagen3 = models.ImageField(upload_to='tours/%Y/%m/%d/')

    def __str__(self):
        return f"Imagen"

    class Meta:
        verbose_name_plural = "Imágenes de Tours"
    
class Resena(models.Model):
    tour = models.ForeignKey(Tour, related_name='resenas', on_delete=models.CASCADE)
    estrellas = models.PositiveIntegerField()
    comentario = models.TextField()

    def __str__(self):
        return f"Reseña para {self.tour.titulo}"
    
class Reserva(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservas')
    codigo_reserva = models.CharField(max_length=85, unique=True)
    nombre = models.CharField(max_length=255)
    dui = models.CharField(max_length=10)  # Asumiendo que el DUI tiene 10 dígitos
    correo_electronico = models.EmailField()
    direccion = models.TextField()
    cantidad_adultos = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    cantidad_ninos = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0)
    fecha_reserva = models.DateField(editable=True)
    qr_code_url = models.URLField(blank=True)
    qr_code = models.ImageField(upload_to='qrcodes', blank=True, null=True)
    
    
    #campos extras
    #lista de tipos de documentos
    DOCUMENTOS_VALIDOS = (
        (' ', ' '),
        ('DUI', 'Documento Unico de Identidad'),
        ('CE', 'Cédula de extrangería'),
        ('LIC', 'Licencia Nacional'),
        ('PA', 'Pasaporte'),
        ('Otro', 'Otro'),
        )
    tipo_documento = models.CharField(max_length=50, choices=DOCUMENTOS_VALIDOS)
    telefono = models.CharField(max_length=15)
    pais_residencia = models.CharField(max_length=50, default="El Salvador")
    
     # Nuevos campos para el total a pagar y el iva
    precio_adulto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nino = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    

    def __str__(self):
        return f"{self.nombre} - {self.tour.titulo}"

    def save(self, *args, **kwargs):
        # Calcular el total a pagar antes de guardar la reserva
        total_sin_iva = self.cantidad_adultos * self.precio_adulto
        iva_calculado = total_sin_iva * Decimal('0.13')  # Calcular el valor del IVA
        self.iva = iva_calculado
        self.total_pagar = total_sin_iva + iva_calculado  # Sumar el IVA al total a pagar
        
        # Generar código de reserva único antes de guardar
        if not self.codigo_reserva:
            self.codigo_reserva = self.generar_codigo_reserva()
            self.enviar_codigo_por_correo()  # Envía el código por correo al crear la reserva
        
        super().save(*args, **kwargs)

    def generar_codigo_reserva(self):
        import random
        from datetime import datetime

        # Obtén la fecha actual en formato YYYYMMDD
        fecha_actual = datetime.now().strftime("%Y%m%d")

        # Genera un número correlativo desde 001
        correlativo = str(random.randint(1, 9999)).zfill(4)

        # Si fecha_reserva es una cadena, conviértela a un objeto datetime
        if isinstance(self.fecha_reserva, str):
            self.fecha_reserva = datetime.strptime(self.fecha_reserva, "%Y-%m-%d")

        # Combina los elementos para formar el código de reserva
        codigo = f"re-{fecha_actual}-{self.fecha_reserva.strftime('%Y%m%d')}-{correlativo}"

        return codigo
    
    def guardar_qr_code_image(self, qr_io):
        from django.core.files.base import ContentFile

        # Guarda la imagen en el sistema de archivos
        image_name = f"qrcode_{self.codigo_reserva}.png"
        self.qr_code.save(image_name, ContentFile(qr_io.getvalue()), save=False)
        self.save()

        # Obtén la URL de la imagen
        return self.qr_code.url

    def enviar_codigo_por_correo(self):
        
        # Crea el mensaje del correo electrónic
        
        # Genera el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.codigo_reserva)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Guarda el código QR en un BytesIO
        qr_io = BytesIO()
        img.save(qr_io)
        qr_io.seek(0)

        # Guarda el código QR en la base de datos y obtén la URL
        self.qr_code_url = self.guardar_qr_code_image(qr_io)

        # Envia el código de reserva y el código QR por correo electrónico
        subject = 'Código de Reserva para el Tour'
        from_email = settings.DEFAULT_FROM_EMAIL  # Cambia esto al remitente real
        to_email = [self.correo_electronico]
                
        # Renderiza el contenido del correo utilizando un template
        context = {
            'tour_titulo': self.tour.titulo,
            'codigo_reserva': self.codigo_reserva,
            'nombre': self.nombre,
            'dui': self.dui,
            'tipo_documento': self.tipo_documento,
            'telefono': self.telefono,
            'correo_electronico': self.correo_electronico,
            'pais_residencia': self.pais_residencia,
            'direccion': self.direccion,
            'cantidad_adultos': self.cantidad_adultos,
            'cantidad_ninos': self.cantidad_ninos,
            'fecha_reserva': self.fecha_reserva,
            'total_pagar': self.total_pagar
        }
        html_content = render_to_string('email/correo_reserva.html', context)
        text_content = strip_tags(html_content)

        # Adjunta la imagen del código QR al mensaje
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.attach(f"qrcode_{self.codigo_reserva}.png", qr_io.getvalue(), "image/png")

        # Adjunta la URL del código QR al mensaje
        msg.attach(f"qrcode_url_{self.codigo_reserva}.txt", self.qr_code_url)

        # Envía el correo
        msg.send()
