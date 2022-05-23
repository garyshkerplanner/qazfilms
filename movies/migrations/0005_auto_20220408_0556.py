# Generated by Django 3.2.6 on 2022-04-07 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20220408_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='movie_url',
            field=models.CharField(default='', max_length=240, verbose_name='MovieUrl'),
        ),
        migrations.AlterField(
            model_name='movies',
            name='trailer_url',
            field=models.CharField(default='', max_length=240, verbose_name='TrailerUrl'),
        ),
        migrations.AlterField(
            model_name='movies',
            name='url',
            field=models.SlugField(max_length=130, unique=True),
        ),
    ]
