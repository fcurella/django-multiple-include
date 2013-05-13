from django.db import models


class Story(models.Model):
    category_slug = models.SlugField()
    title = models.CharField(max_length=100)
