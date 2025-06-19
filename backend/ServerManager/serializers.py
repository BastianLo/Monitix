from rest_framework import serializers
from ServerManager.models import Server, Tag, serverInfo, serverMetric


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        exclude = ["password", "ssh_key"]

class ServerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class ServerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = serverInfo
        exclude = ["server", "id", "created_at", "updated_at"]

class ServerMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = serverMetric
        exclude = ["server", "id"]

class ServerDetailsSerializer(serializers.ModelSerializer):
    serverInfo = ServerInfoSerializer(source='server_info_obj', read_only=True)
    latestMetrics = ServerMetricSerializer(source='latest_server_metric', read_only=True)

    class Meta:
        model = Server
        exclude = ["password", "ssh_key"]
