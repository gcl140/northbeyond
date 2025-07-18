# Generated by Django 5.2.3 on 2025-07-04 12:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coord', '0008_message_replied_at_message_replied_by_message_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='program',
            name='branch',
            field=models.CharField(choices=[('Golden Tulip, DSM', 'Golden Tulip, DSM'), ('Sea Shells, DSM', 'Sea Shells, DSM'), ('Arusha, DSM', 'Arusha, DSM')], max_length=255),
        ),
    ]
