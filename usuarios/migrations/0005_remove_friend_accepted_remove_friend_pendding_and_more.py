# Generated by Django 4.2.2 on 2023-07-04 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_remove_user_friends_user_friend_solicitations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='accepted',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='pendding',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='solicited',
        ),
        migrations.AddField(
            model_name='friend',
            name='situation',
            field=models.CharField(choices=[('Pendente', 'Pendding'), ('Aceito', 'Accepted'), ('Negado', 'Denied')], default='Pendente', max_length=20),
        ),
    ]
