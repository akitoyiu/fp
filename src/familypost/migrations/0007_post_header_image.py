# Generated by Django 3.1.7 on 2021-02-28 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familypost', '0006_auto_20210225_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
