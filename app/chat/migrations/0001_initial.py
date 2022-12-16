# Generated by Django 4.0 on 2022-12-12 11:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9\\_]*$', 'Only alphanumeric characters are allowed.')])),
                ('roomSlug', models.CharField(max_length=30)),
                ('gender', models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)])),
                ('age', models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(18)])),
                ('uuid', models.UUIDField()),
            ],
            options={
                'unique_together': {('username', 'roomSlug')},
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9\\_]*$', 'Only alphanumeric characters are allowed.')])),
                ('online', models.ManyToManyField(blank=True, to='chat.ChatUser')),
            ],
        ),
    ]
