# Generated by Django 5.0 on 2024-02-21 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_comment_comment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_image',
            field=models.ImageField(null=True, upload_to='comment_images'),
        ),
    ]
