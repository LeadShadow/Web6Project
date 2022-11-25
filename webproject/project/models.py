import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.template.defaultfilters import register


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
    phone = models.CharField(max_length=150, null=True)
    birthday = models.DateField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=150, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}:{self.user_id}"

    # @register.filter
    def phone_list(self):
        phones = Phones.objects.filter(user_id=self.user_id, contact_id=self.id).all()
        phones_list = sorted([phone.phone_number for phone in phones])
        return f'{", ".join(sorted(phones_list))}'

    def email_list(self):
        emails = Emails.objects.filter(user_id=self.user_id, contact_id=self.id).all()
        emails_list = sorted([email.mail for email in emails])
        return f'{", ".join(emails_list)}'


class Phones(models.Model):
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    contact = models.ForeignKey(AddressBook, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Emails(models.Model):
    mail = models.CharField(max_length=254, unique=True, null=False)
    contact = models.ForeignKey(AddressBook, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Files(models.Model):
    name = models.CharField(max_length=80, null=True)
    up_id = models.CharField(max_length=35, null=True)
    type = models.CharField(max_length=50, null=True)
    size = models.IntegerField(default=0)
    up_time = models.DateTimeField(default=datetime.datetime.now())
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

