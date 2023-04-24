<<<<<<< HEAD
# Generated by Django 4.0.8 on 2023-04-24 19:23

=======
# Generated by Django 4.1.8 on 2023-04-21 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_report', models.CharField(max_length=100)),
                ('form_name', models.TextField(blank=True, null=True)),
                ('table_content', models.JSONField(blank=True, null=True)),
                ('status', models.CharField(choices=[('On hold', 'On hold'), ('Delivered', 'Delivered'), ('Generated', 'Generated')], default='On hold', max_length=30)),
                ('file_type', models.CharField(blank=True, max_length=30, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='reports/')),
                ('data', models.JSONField(blank=True, null=True)),
                ('language', models.CharField(default='es', max_length=10)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentReportStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_time', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=512)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.taskreport')),
            ],
        ),
    ]
