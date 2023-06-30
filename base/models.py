from django.db import models

from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"


class Sell(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=100, null=False)
    price = models.CharField(max_length=10)
    description = models.TextField(max_length=200, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # image = models.ImageField(default="", null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f"{self.name} : {self.price} \n desc: {self.description} \n by--> {self.user}"

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    product = models.ForeignKey(Sell, on_delete=models.CASCADE, default="")
    body = models.TextField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body[0:50]}"

class Announcement(models.Model):
    aboout = models.TextField(max_length=100)
    startdate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

