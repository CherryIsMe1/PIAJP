import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Task

class TaskBoardAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        response = self.client.get(reverse('taskboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, 'TaskBoard')

    def test_get_tasks_empty(self):
        response = self.client.get(reverse('task_list_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_task_success(self):
        data = {'title': 'Napisać testy jednostkowe'}
        response = self.client.post(
            reverse('task_list_create'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        res_data = response.json()
        self.assertEqual(res_data['title'], 'Napisać testy jednostkowe')
        self.assertFalse(res_data['completed'])
        self.assertTrue(Task.objects.filter(title='Napisać testy jednostkowe').exists())

    def test_create_task_empty_title_validation(self):
        data = {'title': '   '}
        response = self.client.post(
            reverse('task_list_create'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        res_data = response.json()
        self.assertIn('error', res_data)

    def test_patch_task_toggle_completed(self):
        task = Task.objects.create(title='Kupić mleko', completed=False)
        response = self.client.patch(
            reverse('task_detail', args=[task.id]),
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        res_data = response.json()
        self.assertTrue(res_data['completed'])
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_patch_task_not_found(self):
        response = self.client.patch(
            reverse('task_detail', args=[9999]),
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_task_success(self):
        task = Task.objects.create(title='Zadanie do usunięcia')
        response = self.client.delete(reverse('task_detail', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_task_not_found(self):
        response = self.client.delete(reverse('task_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
