# Generated by Django 2.1a1 on 2018-05-26 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_mxmtrack_album_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageevent',
            name='related_track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.MxmTrack'),
        ),
        migrations.AddField(
            model_name='messageevent',
            name='type',
            field=models.CharField(choices=[('LY', 'Lyrics'), ('FA', 'Favorite')], default='LY', max_length=2),
        ),
    ]