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
