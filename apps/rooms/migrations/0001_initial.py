# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 04:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0002_auto_20160610_0344'),
        ('clinics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(blank=True, max_length=35, null=True)),
                ('room', models.CharField(max_length=35)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinics.Clinic')),
            ],
        ),
        migrations.CreateModel(
            name='RoomDoctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.Doctor')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('init', models.TimeField()),
                ('end', models.TimeField()),
                ('week_day', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='roomdoctor',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Schedule'),
        ),
    ]