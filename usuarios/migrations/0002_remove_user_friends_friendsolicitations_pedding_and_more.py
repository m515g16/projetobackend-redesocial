# Generated by Django 4.2.2 on 2023-07-06 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='friends',
        ),
        migrations.AddField(
            model_name='friendsolicitations',
            name='pedding',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Friends',
        ),
    ]
