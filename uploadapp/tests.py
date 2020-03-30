from django.test import Client, TestCase, SimpleTestCase
from .models import Image as Model


class Test(SimpleTestCase):
    allow_database_queries = True

    def setUp(self) -> None:
        Model.objects.get_or_create(hash='firstHash', image='Screenshot_from_2020-02-07_18-22-53.png')
        Model.objects.get_or_create(hash='secondHash', image='Screenshot_from_2020-02-05_18-44-52.png')

    def pages_requests(self):
        c = Client()
        # List
        response = c.get('')
        self.assertEqual(response.status_code, 200)

        # upload
        response = c.get('/upload')
        self.assertEqual(response.status_code, 200)

        # image_hash page
        queries = Model.objects.all()
        self.assertEqual(len(queries), 2)

        for query in queries:
            response = c.get('{}/'.format(query.hash))
            self.assertEqual(response.status_code, 200)

    def test_main_page(self):
        c = Client()
        queries = Model.objects.all()

        response = c.get('')
        object_list = response.context.get('images')
        # Images loaded
        self.assertIsNotNone(response.context.get('images'))
        # All images on the page
        self.assertEqual(len(queries), len(object_list))