from django.contrib import admin
from ServerManager.models import *

# Register your models here.

admin.site.register([
    Server,
    Tag,
    serverInfo,
    serverMetric,
    containerMetric,
    serverContainer
])