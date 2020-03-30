
from django.db import models

from django.db import models


class Image(models.Model):
    hash = models.TextField(primary_key=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.image.name
