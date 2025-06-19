import json
import re
from datetime import datetime

import requests
from ApiManager.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from encrypted_fields.fields import EncryptedTextField


# Create your models here.
def is_color_valid(value):
    if not re.match(r'^#[A-Fa-f0-9]{6}', value):
        raise ValueError(f"{value} is not a valid hex color code.")
    return value



class Server(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    hostname = models.CharField(max_length=100, blank=True, null=True)
    port = models.PositiveIntegerField(default=4589, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    username = models.CharField(max_length=50)
    password = EncryptedTextField(max_length=100, blank=True, null=True)
    ssh_key = EncryptedTextField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='servers', blank=True)
    auth_key = EncryptedTextField(blank=True, null=True)

    last_ping = models.DateTimeField(null=True)
    last_successful_ping = models.DateTimeField(null=True)
    ping_successful = models.BooleanField(default=False)

    auth_type = models.CharField(
        max_length=20,
        choices=[
            ('password', 'Password'),
            ('key', 'SSH Key'),
        ],
        default='password'
    )

    def ping(self):
        #TODO: schema as model field

        try:
            headers = {"AUTHKEY": self.auth_key}
            scheme = "https" if self.port == 443 else "http"
            r = requests.get(f"{scheme}://{self.hostname}:{self.port}/api/server/metrics", headers=headers)
            parsePingResult(self, r.json())
            result = True
        except Exception as e:
            print(e)
            result = False
        self.ping_successful = result
        if result:
            self.last_successful_ping = datetime.now().astimezone()
        self.last_ping = datetime.now().astimezone()
        self.save()
        return result

    def __str__(self):
        return self.name

    @property
    def latest_server_metric(self):
        return self.servermetric_set.order_by('-ts').first()

    @property
    def server_info_obj(self):
        return self.serverinfo_set.first()


def parsePingResult(server, data):
    server_info, created = serverInfo.objects.get_or_create(server=server)
    server_info.hostname = data["host"]["hostname"]
    server_info.os = data["host"]["os"]
    server_info.platform = data["host"]["platform"]
    server_info.platform_family = data["host"]["platformFamily"]
    server_info.platform_version = data["host"]["platformVersion"]
    server_info.kernel_version = data["host"]["kernelVersion"]
    server_info.kernel_arch = data["host"]["kernelArch"]
    server_info.save()

    server_metric, created = serverMetric.objects.get_or_create(server=server, ts=data["ts"])
    server_metric.ram_used = data["memory"]["used"]
    server_metric.ram_available = data["memory"]["available"]
    server_metric.cpu_used = data["cpu"]["usage"]
    server_metric.disk_used = data["disk"]["used"]
    server_metric.disk_available = data["disk"]["free"]
    server_metric.save()

    for container in data["docker"]["stats"]:
        server_container, created = serverContainer.objects.get_or_create(container_id=container["id"], server=server)
        server_container.name = container["name"]
        server_container.image = container["image"]
        server_container.state = container["state"]
        server_container.save()

        container_metrics, created = containerMetric.objects.get_or_create(container=server_container, ts=data["ts"])
        container_metrics.ram_used = container["ram"]
        container_metrics.cpu_used = container["cpu"]
        container_metrics.save()

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, validators=[RegexValidator(regex=r'^#[A-Fa-f0-9]{6}')], default='#FFFFFF')

    def __str__(self):
        return self.name

class serverInfo(BaseModel):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    hostname = models.CharField(max_length=200, null=True)
    os = models.CharField(max_length=40, null=True)
    platform = models.CharField(max_length=40, null=True)
    platform_family = models.CharField(max_length=40, null=True)
    platform_version = models.CharField(max_length=40, null=True)
    kernel_version = models.CharField(max_length=40, null=True)
    kernel_arch = models.CharField(max_length=40, null=True)

    def __str__(self):
        return str(self.server) + " - " + self.hostname

class serverMetric(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    ts = models.DateTimeField(null=True)
    ram_used = models.BigIntegerField(null=True)
    ram_available = models.BigIntegerField(null=True)
    cpu_used = models.FloatField(null=True)
    disk_used = models.BigIntegerField(null=True)
    disk_available = models.BigIntegerField(null=True)

    def __str__(self):
        return str(self.server) + " - " + timezone.localtime(self.ts, timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S')

class serverContainer(BaseModel):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    container_id = models.CharField(max_length=200, unique=True)
    image = models.CharField(max_length=200)
    state = models.CharField(max_length=50)

    def __str__(self):
        return str(self.server) + " - " + self.name

class containerMetric(models.Model):
    container = models.ForeignKey(serverContainer, on_delete=models.CASCADE)
    ts = models.DateTimeField(null=True)
    ram_used = models.BigIntegerField(null=True)
    cpu_used = models.FloatField(null=True)

    def __str__(self):
        return self.container.name + " - " + timezone.localtime(self.ts, timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S')
