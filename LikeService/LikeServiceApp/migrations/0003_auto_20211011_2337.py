# Generated by Django 3.2.7 on 2021-10-11 20:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('LikeServiceApp', '0002_auto_20211011_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='postID',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='like',
            name='userID',
            field=models.PositiveBigIntegerField(),
        ),
    ]
