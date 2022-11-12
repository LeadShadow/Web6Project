from django.forms import ModelForm
from .models import Tag, Note, AddressBook


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['name', 'description']
        exclude = ['tags']


class ABForm(ModelForm):
    class Meta:
        model = AddressBook
        fields = ['name']
