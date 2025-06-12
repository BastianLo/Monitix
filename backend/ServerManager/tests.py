from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ServerManager.models import Server, Tag

class ServerAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.server_data = {
            'name': 'test-server',
            'hostname': 'example.com',
            'port': 22,
            'username': 'user',
            'password': 'pass',
            'auth_type': 'password'
        }
        self.tag_data = {
            'name': 'test-tag',
            'color': '#FFFFFF'
        }

    def test_create_server(self):
        response = self.client.post('/api/server/', self.server_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Server.objects.count(), 1)
        self.assertEqual(Server.objects.get().name, 'test-server')

    def test_list_servers(self):
        Server.objects.create(**self.server_data)
        response = self.client.get('/api/server/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_server(self):
        server = Server.objects.create(**self.server_data)
        response = self.client.get(f'/api/server/{server.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test-server')

    def test_update_server(self):
        server = Server.objects.create(**self.server_data)
        update_data = {'name': 'updated-server'}
        response = self.client.patch(f'/api/server/{server.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        server.refresh_from_db()
        self.assertEqual(server.name, 'updated-server')

    def test_delete_server(self):
        server = Server.objects.create(**self.server_data)
        response = self.client.delete(f'/api/server/{server.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Server.objects.count(), 0)

class TagAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag_data = {
            'name': 'test-tag',
            'color': '#FFFFFF'
        }

    def test_create_tag(self):
        response = self.client.post('/api/tags/', self.tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().name, 'test-tag')

    def test_list_tags(self):
        Tag.objects.create(**self.tag_data)
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_tag(self):
        tag = Tag.objects.create(**self.tag_data)
        response = self.client.get(f'/api/tags/{tag.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test-tag')

    def test_update_tag(self):
        tag = Tag.objects.create(**self.tag_data)
        update_data = {'name': 'updated-tag'}
        response = self.client.patch(f'/api/tags/{tag.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, 'updated-tag')

    def test_delete_tag(self):
        tag = Tag.objects.create(**self.tag_data)
        response = self.client.delete(f'/api/tags/{tag.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)
