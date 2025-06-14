from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not Schedule.objects.filter(name='ping_server').exists():
            schedule(
                'ServerManager.tasks.ping_server',
                schedule_type='I',
                minutes=1,
                repeats=-1,
                name='ping_server',
            )
            self.stdout.write("Scheduled ping_server.")
        else:
            self.stdout.write("ping_server already scheduled.")