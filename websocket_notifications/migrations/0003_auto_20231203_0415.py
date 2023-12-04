# Generated by Django 4.2.5 on 2023-12-03 10:15

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models


def transform_user_to_generic_object(apps, schema_editor):
    NotificationGroup = apps.get_model("websocket_notifications.NotificationGroup")
    User = get_user_model()
    user_content_type = ContentType.objects.get_for_model(User)

    for group in NotificationGroup.objects.filter(user_id__isnull=False):
        group.content_type = user_content_type
        group.object_id = group.user_id
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ("websocket_notifications", "0002_alter_notificationgroup_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="notificationgroup",
            name="content_type",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to="contenttypes.ContentType",
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="notificationgroup",
            name="object_id",
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.RunPython(
            transform_user_to_generic_object, reverse_code=migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name="notificationgroup",
            name="user",
        ),
    ]
