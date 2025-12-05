from django.db import models
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    @property
    def rating(self):
        return self.reviews.aggregate(avg=Avg('stars'))['avg']

    def __str__(self):
        return self.title


class Review(models.Model):

    STARS = [(i, i) for i in range(1, 6)]

    stars = models.IntegerField(choices=STARS, default=3)
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True)

    def __str__(self):
        return self.text