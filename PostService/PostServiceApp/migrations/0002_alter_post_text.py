# Generated by Django 3.2.7 on 2021-10-13 21:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('PostServiceApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=500),
        ),
    ]
