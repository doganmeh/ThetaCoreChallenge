from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from expert import models


class ExpertModelTests(TestCase):
    def test_short_url(self):
        expert = models.Expert.objects.create(
            name='Jane Doe',
            long_url='https://www.google.com/'
        )
        from urllib import request
        response = request.urlopen(expert.short_url)
        self.assertEqual(expert.long_url, response.url)
    
    def test_strip_non_header_text(self):
        html = '<h1>MEHMET</h1><h2 class="nonsense">' \
               'serdar</h2><h4>not-dogan</h4>><h3><strong>dogan<strong></h3>'
        stripped = models.Expert.strip_non_header_text(html)
        expected = "h1: mehmet\nh2: serdar\nh3: dogan"
        self.assertEqual(stripped, expected)


def get_url(app, model, action, kwargs=None):
    if kwargs is None:
        kwargs = {}
    url_name = app + ":" + model + "-" + action
    return reverse(url_name, kwargs=kwargs)


class TestExpertCrudViews(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
    
    @classmethod
    def setUpTestData(cls):
        cls.app_name = 'expert'
        cls.model_name = 'expert'
        cls.obj = models.Expert.objects.create(
            **{
                'name'    : 'John Doe',
                'long_url': 'https://www.edgle.com/',
            }
        )
        cls.right_data = {
            'name'    : 'Jane Doe',
            'long_url': 'http://www.harmonytx.org/',
        }
        cls.wrong_data = [
            {
                # 'name'    : None,
                'long_url': 'http://www.harmonytx.org/',
            },
            {
                'name'    : 'Jane Doe',
                # 'long_url': None,
            },
        ]
    
    def setUp(self):
        settings.DEBUG = True  # somehow django has DEBUG=False by default for tests
        # self.client.login(username='testuser', password='t11111111')
    
    def test_get_create(self):
        url = get_url(self.app_name, self.model_name, "create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_create_success(self):
        create_url = get_url(self.app_name, self.model_name, "create")
        list_url = get_url(self.app_name, self.model_name, "list")
        url = create_url + '?next=' + list_url
        response = self.client.post(url, self.right_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, list_url)
    
    def test_post_create_failure(self):
        create_url = get_url(self.app_name, self.model_name, "create")
        
        if not isinstance(self.wrong_data, list):
            self.wrong_data = [self.wrong_data]
        
        for wd in self.wrong_data:
            wd['pk'] = self.obj.pk  # create
            response = self.client.post(create_url, wd)
            self.assertEqual(response.status_code, 200)
            self.assertIn('This field is required', str(response.content))
    
    def test_get_update(self):
        url = get_url(self.app_name, self.model_name, "update", kwargs={'pk': self.obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_update_success(self):
        update_url = get_url(self.app_name, self.model_name, "update", kwargs={'pk': self.obj.pk})
        list_url = get_url(self.app_name, self.model_name, "list")
        self.right_data['pk'] = self.obj.pk  # update
        url = update_url + '?next=' + list_url
        response = self.client.post(url, self.right_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, list_url)
    
    def test_post_update_failure(self):
        update_url = get_url(self.app_name, self.model_name, "update", kwargs={'pk': self.obj.pk})
        
        if not isinstance(self.wrong_data, list):
            self.wrong_data = [self.wrong_data]
        
        for wd in self.wrong_data:
            wd['pk'] = self.obj.pk  # update
            response = self.client.post(update_url, wd)
            self.assertEqual(response.status_code, 200)
            self.assertIn('This field is required', str(response.content))
    
    def test_get_delete(self):
        delete_url = get_url(self.app_name, self.model_name, "delete", kwargs={'pk': self.obj.pk})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_delete(self):
        delete_url = get_url(self.app_name, self.model_name, "delete", kwargs={'pk': self.obj.pk})
        list_url = get_url(self.app_name, self.model_name, "list")
        url = delete_url + '?next=' + list_url
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, list_url)
    
    def test_get_detail(self):
        url = get_url(self.app_name, self.model_name, "detail", kwargs={'pk': self.obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('detail', str(response.content).lower())
    
    def test_get_list(self):
        url = get_url(self.app_name, self.model_name, "list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('list', str(response.content).lower())
