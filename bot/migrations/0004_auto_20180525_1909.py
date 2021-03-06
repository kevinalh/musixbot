# Generated by Django 2.1a1 on 2018-05-26 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_mxmtrack_spotify_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mxmtrack',
            name='image_url',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='mxmtrack',
            name='spotify_url',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='mxmtrack',
            name='track_url',
            field=models.URLField(default='https://www.musixmatch.com/', max_length=500),
        ),
    ]
