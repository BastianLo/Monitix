from django.contrib import admin
from ServerManager.models import Server, Tag

# Register your models here.

admin.site.register([
    Server,
    Tag
])