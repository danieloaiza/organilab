# Generated by Django 4.0.8 on 2022-11-08 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('laboratory', '0058_organizationstructure_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationStructureRelations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratory.organizationstructure', verbose_name='Organization')),
            ],
        ),
        migrations.AddIndex(
            model_name='organizationstructurerelations',
            index=models.Index(fields=['content_type', 'object_id'], name='laboratory__content_d54116_idx'),
        ),
    ]
