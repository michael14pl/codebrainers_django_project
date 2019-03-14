from django.db import models
from django.db.models import deletion
from django.urls import reverse


class Post(models.Model):
    text = models.TextField(blank=False, default='')
    title = models.CharField(max_length=128, blank=False, default='')
    votes = models.IntegerField(blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("accounts.User", deletion.PROTECT, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:details", args=(self.pk, ))
