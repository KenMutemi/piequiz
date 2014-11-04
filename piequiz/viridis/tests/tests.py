from django.test import TestCase
from viridis.models import Test, Question, Choice


class TestViewsTestCase(TestCase):
    def test_quiz_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_add_quiz(self):
        resp = self.client.get('/quiz/new')
        self.assertEqual(resp.status_code, 302)

    def test_add_questions(self):
        resp = self.client.get('/questions/add')
        self.assertEqual(resp.status_code, 302)

    def test_add_choices(self):
        resp = self.client.get('/choices/add')
        self.assertEqual(resp.status_code, 302)

    def test_quiz_detail(self):
        resp = self.client.get('/1/physics/')	
        self.assertEqual(resp.status_code, 302)
	# A 301 for permanent redirect
        resp = self.client.get('/1/')
        self.assertEqual(resp.status_code, 301)

    def test_call_view_denies_anonymous(self):
        response = self.client.get('/3/biology/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/3/biology/')

        response = self.client.get('/quiz/new', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/quiz/new')

        response = self.client.get('/questions/add', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/questions/add')

        response = self.client.get('/profile/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

        response = self.client.get('/avatar/change/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/avatar/change/')

        response = self.client.get('/avatar/add/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/avatar/add/')
