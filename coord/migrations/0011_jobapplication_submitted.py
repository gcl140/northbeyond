# Generated by Django 5.2.3 on 2025-07-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coord', '0010_jobapplication_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
    ]
