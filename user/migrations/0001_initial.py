# Generated by Django 2.2.12 on 2020-05-09 04:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=16, verbose_name='ユーザー名')),
                ('image', models.ImageField(null=True, upload_to='profile_images', verbose_name='プロフィール画像')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='メールアドレス')),
                ('introduction', models.CharField(max_length=128, null=True, verbose_name='自己紹介')),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]