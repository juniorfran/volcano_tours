# Generated by Django 4.2.9 on 2024-01-24 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transacciones', '0009_rename_imagen_enlacepago_imagenproducto'),
    ]

    operations = [
        migrations.AddField(
            model_name='enlacepago',
            name='idEnlace',
            field=models.CharField(default=222222, max_length=150),
            preserve_default=False,
        ),
    ]
