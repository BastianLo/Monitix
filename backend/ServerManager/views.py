from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ServerManager.models import Server
from ServerManager.serializers import *

# Create your views here.


@api_view(['POST'])
def execute_command(request, id): #create a server via api
    print(request)
    return Response({
        'status': 'Command successfully executed',
    }, status=200)

class ServerViewset(GenericViewSet):

    queryset = Server.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ServerCreateSerializer
        return ServerSerializer

    # def get_permissions(self):
    #     return [IsAuthenticated]

    def get_permissions(self):
        permission_classes = [] #[IsAuthenticated]
        return [permission() for permission in permission_classes]
    def list(self, request):
        results = Server.objects.all()
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data, status=200)


    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            server = self.queryset.get(pk=pk)
            serializer = self.get_serializer(server)
            return Response(serializer.data, status=200)
        except Server.DoesNotExist:
            return Response({"detail": "Server not found"}, status=status.HTTP_404_NOT_FOUND)
        pass

    def update(self, request, pk=None):
        try:
            server = self.queryset.get(pk=pk)
            serializer = self.get_serializer(server, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        except Server.DoesNotExist:
            return Response({"detail": "Server not found"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            server = self.queryset.get(pk=pk)
            serializer = self.get_serializer(server, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        except Server.DoesNotExist:
            return Response({"detail": "Server not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            server = self.queryset.get(pk=pk)
            server.delete()
            return Response({"detail": "Server deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Server.DoesNotExist:
            return Response({"detail": "Server not found"}, status=status.HTTP_404_NOT_FOUND)

class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        permission_classes = [] #[IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        results = Tag.objects.all()
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data, status=200)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def retrieve(self, request, pk=None):
        try:
            tag = self.queryset.get(pk=pk)
            serializer = self.get_serializer(tag)
            return Response(serializer.data, status=200)
        except Tag.DoesNotExist:
            return Response({"detail": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
    def update(self, request, pk=None):
        try:
            tag = self.queryset.get(pk=pk)
            serializer = self.get_serializer(tag, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        except Tag.DoesNotExist:
            return Response({"detail": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
    def partial_update(self, request, pk=None):
        try:
            tag = self.queryset.get(pk=pk)
            serializer = self.get_serializer(tag, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        except Tag.DoesNotExist:
            return Response({"detail": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, pk=None):
        try:
            tag = self.queryset.get(pk=pk)
            tag.delete()
            return Response({"detail": "Tag deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist:
            return Response({"detail": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)