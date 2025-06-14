from datetime import date, datetime

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ServerManager.models import Server


@receiver(post_save, sender=Server)
def save_user_profile(sender, instance, **kwargs):
    if instance.last_ping:
        seconds_since_last_ping = (datetime.now().astimezone() - instance.last_ping).total_seconds()
        if seconds_since_last_ping > 1:
            instance.ping()
    else:
        instance.ping()
