# Generated by Django 5.2.2 on 2025-06-13 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServerManager', '0003_server_last_ping_server_ping_successful'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='last_ping',
            field=models.DateTimeField(),
        ),
    ]
