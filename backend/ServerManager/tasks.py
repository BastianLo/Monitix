from django.contrib.messages import success
from ServerManager.models import Server
from datetime import datetime

def ping_server():
    servers = Server.objects.all()
    total = servers.count()
    success = 0
    for server in servers:
        ping_result = server.ping()
        if ping_result:
            success += 1
    return f"Pinged {success} out of {total} servers successfully."
