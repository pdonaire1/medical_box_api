# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-03 05:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0001_initial'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('paid', models.BooleanField()),
                ('note', models.TextField(blank=True, null=True)),
                ('recipe', models.TextField(blank=True, null=True)),
                ('consult', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.DoctorSpeciality')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.Patient')),
            ],
        ),
    ]
