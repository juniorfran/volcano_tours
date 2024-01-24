# Generated by Django 5.0.1 on 2024-01-04 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('duracion', models.PositiveIntegerField()),
                ('iva', models.BooleanField(default=False)),
                ('imagen', models.ImageField(upload_to='tours')),
                ('tipo_tour', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tours.tipotour')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='tours/%Y/%m/%d/')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='Tours.tour')),
            ],
        ),
    ]