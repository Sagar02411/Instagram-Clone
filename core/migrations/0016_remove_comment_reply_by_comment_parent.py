# Generated by Django 5.0 on 2024-01-30 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_comment_reply_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply_by',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_parent', to='core.comment'),
        ),
    ]