# Generated by Django 4.0.4 on 2022-05-23 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_reviews'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reviews',
        ),
    ]