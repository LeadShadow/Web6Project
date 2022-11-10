import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=25, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}:{self.user_id}"


class Note(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}:{self.user_id}"


class AddressBook(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=150, null=False)
    birthday = models.DateTimeField(max_length=50)
    email = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=150, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}:{self.user_id}"


class Files(models.Model):
    title = models.CharField(max_length=50)
    upload = models.FileField(upload_to="media")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
