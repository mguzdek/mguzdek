from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

def upload_location(instance, filename):
    return "%s/%S" %(instance.id, filename)

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    #slug = models.SlugField(unique=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(
            upload_to=upload_location,
            null=True,
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]
