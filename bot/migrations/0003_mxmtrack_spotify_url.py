# Generated by Django 2.1a1 on 2018-05-25 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_mxmtrack_track_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='mxmtrack',
            name='spotify_url',
            field=models.URLField(blank=True),
        ),
    ]
