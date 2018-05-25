# Generated by Django 2.1a1 on 2018-05-24 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_messageevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='MxmTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commontrack_id', models.PositiveIntegerField()),
                ('track_name', models.TextField()),
                ('artist_name', models.TextField()),
            ],
        ),
    ]
