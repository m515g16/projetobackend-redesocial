# Generated by Django 4.2.2 on 2023-07-03 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_follower_friend_remove_user_follower_friend_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follower',
            old_name='seguidor',
            new_name='follower',
        ),
        migrations.RenameField(
            model_name='follower',
            old_name='usuario',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='friend',
            old_name='usuario',
            new_name='user',
        ),
    ]
