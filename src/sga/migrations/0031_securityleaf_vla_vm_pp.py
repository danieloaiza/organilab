# Generated by Django 3.2 on 2022-10-14 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sga', '0030_auto_20221014_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='securityleaf',
            name='vla_vm_pp',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='VLA-VM[ppm]'),
        ),
    ]
