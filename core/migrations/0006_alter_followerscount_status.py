# Generated by Django 5.0 on 2024-02-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_followerscount_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followerscount',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
