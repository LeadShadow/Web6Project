from django.contrib import admin
from .models import Tag, Note, AddressBook, Files


# Register your models here.
admin.site.register(Tag)
admin.site.register(Note)
admin.site.register(AddressBook)
admin.site.register(Files)
