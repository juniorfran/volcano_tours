# Generated by Django 4.2.9 on 2024-01-12 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuraciones', '0002_alter_team_bar_team_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='barra_principal',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-12 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contacts',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-12 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urls_info',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-12 00:00:00'),
            preserve_default=False,
        ),
    ]