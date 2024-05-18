from django.test import TestCase

class MyViewTest(TestCase):

    def test_homepage_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_book_list_returns_200(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

    def test_bookpage_with_id_returns_200(self):
        response = self.client.get('/book?id=64977f9c40ed60d37020b682')
        self.assertEqual(response.status_code, 200)

    def test_create_book_page_returns_200(self):
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
