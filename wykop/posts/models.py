from django.db import models


class Post(models.Model):
    text = models.TextField(blank=False, default='')
    title = models.CharField(max_length=128, blank=False, default='')
    votes = models.IntegerField(blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
