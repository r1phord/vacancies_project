# Generated by Django 3.0.7 on 2020-07-01 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0003_auto_20200701_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialty',
            name='picture',
            field=models.ImageField(upload_to='speciality_images'),
        ),
    ]
