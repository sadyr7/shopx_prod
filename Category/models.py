from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True,blank=True)
    img = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class PodCategory(models.Model):
    category = models.ForeignKey(
        Category, related_name="pod_categories", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "podcategory"
        verbose_name_plural = "podcategory"

    def __str__(self):
        return self.name