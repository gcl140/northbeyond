# Generated by Django 5.2.3 on 2025-06-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coord', '0004_upcomingevent_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='upcomingevent',
            name='location',
            field=models.CharField(default='Golden Tulip, DSM', max_length=255),
        ),
    ]
