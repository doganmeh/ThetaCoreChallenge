from django.test import TestCase

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
               'serdar</h2><h3>not-dogan</h3>><h2><strong>dogan<strong></h2>'
        stripped = models.Expert.strip_non_header_text(html)
        expected = "h1: mehmet\nh2: serdar\nh2: dogan"
        self.assertEqual(stripped, expected)
