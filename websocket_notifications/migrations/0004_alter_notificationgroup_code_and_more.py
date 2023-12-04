# Generated by Django 4.2.5 on 2023-12-04 01:44

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("websocket_notifications", "0003_auto_20231203_0415"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notificationgroup",
            name="code",
            field=models.UUIDField(default=uuid.uuid4, verbose_name="code"),
        ),
        migrations.AlterField(
            model_name="notificationgroup",
            name="object_id",
            field=models.CharField(max_length=256),
        ),
    ]