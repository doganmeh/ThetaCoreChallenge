import datetime

from django.conf import settings
from django.db import models
from django.utils.timezone import make_aware


class Expert(models.Model):
    # user editable fields
    name = models.CharField(max_length=100, null=False, blank=False)
    friends = models.ManyToManyField('self', blank=True)
    long_url = models.URLField(verbose_name='URL', null=False, blank=False)
    # non user editable fields
    short_url = models.URLField(null=True, blank=True)
    heading_text = models.TextField(null=True, blank=True)
    # there is no need for related_name because friendships are bi-directional
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(null=True, blank=True)
    
    def header_count(self):
        return len(self.heading_text.split('\n'))
    
    def friend_count(self):
        return len(self.friends.all())
    
    def __str__(self):
        return self.name + " (" + self.short_url + ")"
    
    @classmethod
    def strip_non_header_text(cls, raw_header):
        import re
        headers = re.findall('<(h1|h2).*?>(.+?)</(h1|h2)>', raw_header)
        headers = [header[0] + ': ' + re.sub('<.*?>', '', header[1]) + '<br/>' for header in
                   headers]
        return '\n'.join(headers).lower()
    
    def save(self, *args, **kwargs):
        original = None
        if self.pk is not None:  # being updated
            self.modified = make_aware(datetime.datetime.now())
            original = Expert.objects.get(pk=self.pk)
        
        # shorten url
        if original is None or self.long_url != original.long_url:
            import bitly_api
            conn = bitly_api.Connection(access_token=settings.BITLY_ACCESS_TOKEN)
            self.short_url = conn.shorten(uri=self.long_url)['url']
        
        # get heading text
        if original is None or self.long_url != original.long_url:
            from urllib import request
            response = request.urlopen(self.long_url)
            html = response.read()
            charset = response.info().get_charset()
            if charset is None:
                charset = 'latin-1'
                # see: https://stackoverflow.com/a/25759213/2863603
            html = html.decode(charset)
            self.heading_text = self.strip_non_header_text(html)
        super().save(*args, **kwargs)
