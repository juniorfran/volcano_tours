# Generated by Django 4.2.9 on 2024-01-23 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Transacciones', '0002_remove_enlacepago_cantidad_maxima_cuotas_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enlacepago',
            name='cantidad_por_defecto',
        ),
        migrations.RemoveField(
            model_name='enlacepago',
            name='descripcion_producto',
        ),
        migrations.RemoveField(
            model_name='enlacepago',
            name='emails_notificacion',
        ),
        migrations.RemoveField(
            model_name='enlacepago',
            name='es_cantidad_editable',
        ),
        migrations.RemoveField(
            model_name='enlacepago',
            name='es_monto_editable',
        ),
        migrations.RemoveField(
            model_name='enlacepago',
            name='notificar_transaccion_cliente',
        ),
        migrations.RemoveField(
            model_name='enlacepago',
            name='telefonos_notificacion',
        ),
        migrations.RemoveField(
            model_name='enlacepago',
            name='url_imagen_producto',
        ),
    ]
