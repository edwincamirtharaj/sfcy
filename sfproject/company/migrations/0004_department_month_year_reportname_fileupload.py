# Generated by Django 5.0.1 on 2024-02-01 10:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_remove_usercompanymapping_confirmation_token_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('show_field', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('show_field', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.department')),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('file_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('show_field', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('extra_field1', models.CharField(blank=True, max_length=255, null=True)),
                ('extra_field2', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.month')),
                ('reports_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.reportname')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.year')),
            ],
        ),
    ]
