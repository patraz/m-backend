from typing import Iterable, Optional
from django.db import models
from django.utils.text import slugify
# Create your models here.

class Definition(models.Model):
    word = models.CharField(max_length=300)
    meaning = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.word)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.word