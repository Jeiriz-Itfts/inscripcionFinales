# Generated by Django 3.2.8 on 2021-10-24 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inscripcionFinales', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='fecha_creación',
            new_name='fecha_creacion',
        ),
    ]
