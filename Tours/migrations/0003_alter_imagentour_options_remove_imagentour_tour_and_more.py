# Generated by Django 5.0.1 on 2024-01-08 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tours', '0002_resena'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagentour',
            options={'verbose_name_plural': 'Imágenes de Tours'},
        ),
        migrations.RemoveField(
            model_name='imagentour',
            name='tour',
        ),
        migrations.AddField(
            model_name='tour',
            name='imagenes',
            field=models.ManyToManyField(related_name='tours', to='Tours.imagentour'),
        ),
    ]