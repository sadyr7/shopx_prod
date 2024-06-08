from django.db import models


class Baner(models.Model):
    title = models.CharField(max_length=255)
    image  = models.ImageField(upload_to="baner/%Y/%m/%d/")

    def __str__(self) -> str:
        return f"{self.title}"

