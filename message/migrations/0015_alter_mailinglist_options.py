# Generated by Django 4.2.2 on 2024-08-28 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("message", "0014_alter_mailinglist_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailinglist",
            options={
                "permissions": [
                    ("can_edit_status", "can_edit_status"),
                    ("can_edit_toggle_status", "can_edit_toggle_status"),
                ],
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
    ]
