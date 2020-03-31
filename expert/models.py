import datetime

from django.conf import settings
from django.db import models
from django.utils.timezone import make_aware


class Expert(models.Model):
    # user editable fields
    name = models.CharField(max_length=100, null=False, blank=False)
    friends = models.ManyToManyField('self')
    long_url = models.URLField(verbose_name='URL', null=False, blank=False)
    # non user editable fields
    short_url = models.URLField(null=True, blank=True)
    heading_text = models.TextField(null=True, blank=True)
    # there is no need for related_name because friendships are bi-directional
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(null=True, blank=True)
    
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
            pass
        
        super().save(*args, **kwargs)
