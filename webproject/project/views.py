from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Tag, Note, User, Files


# Create your views here.

def signupuser(request):
    pass


def loginuser(request):
    pass


@login_required
def logoutuser(request):
    pass


def main(request):
    pass


@login_required
def detail_note(request, note_id):
    pass


@login_required
def tag(request):
    pass


@login_required
def note(request):
    pass


@login_required
def show_notes(request):
    pass


@login_required
def set_done_note(request, note_id):
    pass


@login_required
def delete_note(request, note_id):
    pass


@login_required
def detail_note(request, note_id):
    pass


@login_required
def addressbook(request):
    pass


@login_required
def edit_ab(request, ad_id):
    pass


@login_required
def delete_ab(request, ad_id):
    pass


@login_required
def set_done_ab(request, note_id):
    pass


@login_required
def show_addressbook(request):
    pass


@login_required
def download_files(request):
    pass

