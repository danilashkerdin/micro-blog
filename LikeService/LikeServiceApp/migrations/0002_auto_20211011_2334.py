# Generated by Django 3.2.7 on 2021-10-11 20:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('LikeServiceApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postID', models.IntegerField()),
                ('userID', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Hero',
        ),
    ]
