from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watch_list = models.ManyToManyField('Listing', related_name="watchers")


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_price = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name="listings", null=True)
    image_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    content = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.author} on {self.listing}: {self.content}"

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self) -> str:
        return self.name

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="bids", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

