from rest_framework import serializers
from ServerManager.models import Server, Tag


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