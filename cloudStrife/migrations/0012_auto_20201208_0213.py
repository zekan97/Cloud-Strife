# Generated by Django 3.1.1 on 2020-12-08 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloudStrife', '0011_auto_20201130_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador', to='cloudStrife.usuario'),
        ),
    ]