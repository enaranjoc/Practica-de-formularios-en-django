# Generated by Django 4.1.3 on 2022-12-02 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='imagen',
            field=models.ImageField(default='imagen', upload_to='imagenes/'),
        ),
    ]
