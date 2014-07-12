from django.test import TestCase
from viridis.models import Test, Question, Choice

class TestListViewTestCase(TestCase):
    def test_quiz_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_add_quiz(self):
        resp = self.client.get('/test/new')
        self.assertEqual(resp.status_code, 302)

    def test_add_questions(self):
        resp = self.client.get('/question/new')
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

# Create your tests here.
