# доп задание на зачет tests

from rest_framework.test import APITestCase
from rest_framework import status

from notes_app.models import Note
from django.contrib.auth.models import User


class TestNotesListCreateAPIView(APITestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_note_create(self):
        self.assertTrue(self.client.login(username='testuser', password='secret'))

        data = {
            "title": "5",
            "message": "cdgf0000000aga",
            "public": False,
            "importance": False,
            "condition": 1,
            "author": 1
        }
        path = "/notes/"
        resp = self.client.post(path, data=data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.get(id=1).title, "5")

    def test_note_put_by_author(self):
        self.credentials = {
            'username': 'testuser2',
            'password': 'secret2'}
        user2 = User.objects.create_user(**self.credentials)
        self.assertTrue(self.client.login(username='testuser2', password='secret2'))

        Note.objects.create(title="test2", author=user2)

        data = {
            "title": "5adadas",
            "message": "cdgf0000000aga",
            "public": False,
            "importance": False,
            "condition": 1,
            "date_and_time": "2022-06-03T19:28:00",
            "author": 2
        }

        path = "/notes/1"
        resp = self.client.put(path=path, data=data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Note.objects.get(id=1).title, "5adadas")

    def test_note_put_NOT_by_author(self):
        self.credentials = {
            'username': 'testuser2',
            'password': 'secret2'}
        User.objects.create_user(**self.credentials)
        self.assertTrue(self.client.login(username='testuser2', password='secret2'))

        Note.objects.create(title="test2", author_id=1)
        print(Note.objects.get(id=1).author)

        data = {
            "title": "5adadas",
            "message": "cdgf0000000aga",
            "public": False,
            "importance": False,
            "condition": 1,
            "date_and_time": "2022-06-03T19:28:00",
        }

        path = "/notes/1"
        resp = self.client.put(path=path, data=data)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Note.objects.get(id=1).title, "test2")
        self.assertNotEquals(Note.objects.get(id=1).title, "5adadas")

    def test_delete_by_author(self):
        self.assertTrue(self.client.login(username='testuser', password='secret'))

        Note.objects.create(title="test2", author_id=1)
        path = "/notes/1"
        resp = self.client.delete(path=path)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_not_by_author(self):
        self.credentials = {
            'username': 'testuser2',
            'password': 'secret2'}
        User.objects.create_user(**self.credentials)
        self.assertTrue(self.client.login(username='testuser2', password='secret2'))

        Note.objects.create(title="test2", author_id=1)
        path = "/notes/1"
        resp = self.client.delete(path=path)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
