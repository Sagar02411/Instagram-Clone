# Generated by Django 5.0 on 2023-12-29 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_follow_followingcount_remove_followerscount_follower_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
        migrations.DeleteModel(
            name='FollowingCount',
        ),
        migrations.RemoveField(
            model_name='followerscount',
            name='user_follower_count',
        ),
        migrations.AddField(
            model_name='followerscount',
            name='follower',
            field=models.CharField(default='name', max_length=100),
        ),
    ]
