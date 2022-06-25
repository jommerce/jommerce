# Generated by Django 4.0.3 on 2022-04-30 00:51

from django.db import migrations, models
from djplus.auth.validators import get_password_validators, get_username_validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, validators=get_username_validators(), verbose_name='username')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='email')),
                ('password', models.CharField(max_length=128, validators=get_password_validators(), verbose_name='password')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
