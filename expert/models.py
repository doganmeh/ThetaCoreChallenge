import datetime

from django.db import models


class Expert(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    friends = models.ManyToManyField('self')
    url = models.URLField(null=False, blank=False)
    # non user editable fields
    url_short = models.URLField(null=True, blank=True)
    heading_text = models.TextField(null=True, blank=True)
    # there is no need for related_name because friendships are bi-directional
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=None)
    
    def save(self, *args, **kwargs):
        original = None
        if self.pk is not None:  # being updated
            self.modified = datetime.datetime.now
            original = Expert.objects.get(pk=self.pk)
        
        # shorten url
        if original is None or self.url != original.url:
            pass
        
        # get heading text
        if original is None or self.url != original.url:
            pass
        
        super().save(*args, **kwargs)
