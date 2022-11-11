from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import IntegrityError
from .models import Tag, Note, User, Files


# Create your views here.

def user_signup(request):
    if request.method == 'GET':
        return render(request, 'project/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('user_login')
            except IntegrityError as err:
                return render(request, 'project/signup.html',
                              {'form': UserCreationForm(), 'error': 'Username already exist!'})
        else:
            return render(request, 'project/signup.html',
                          {'form': UserCreationForm(), 'error': 'Password did not match'})


def user_login(request):
    if request.method == 'GET':
        return render(request, 'project/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'project/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password didn\'t match'})
        login(request, user)
        return redirect('main')


@login_required
def user_logout(request):
    logout(request)
    return redirect('main')


def main(request):
    return render(request, 'project/index.html', {})


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
