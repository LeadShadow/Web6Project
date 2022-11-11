from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Tag, Note, User, Files
from .forms import TagForm, NoteForm


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
    notes = []
    if request.user.is_authenticated:
        notes = Note.objects.filter(user_id=request.user).all()
    return render(request, 'project/base.html', {"notes": notes})


@login_required
def detail_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user_id=request.user)
    note.tag_list = ', '.join([str(name) for name in note.tags.all()])
    return render(request, 'project/notes.html', {"note": note})


@login_required
def tag(request):
    if request.method == 'POST':
        try:
            form = TagForm(request.POST)
            tag = form.save(commit=False)
            tag.user_id = request.user
            tag.save()
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'project/add_tags.html', {'form': TagForm(), 'error': err})
        except IntegrityError as err:
            return render(request, 'project/add_tags.html', {'form': TagForm(), 'error': 'Tag already exists!'})
    return render(request, 'project/add_tags.html', {'form': TagForm()})


@login_required
def note(request):
    tags = Tag.objects.filter(user_id=request.user).all()

    if request.method == 'POST':
        try:
            list_tags = request.POST.getlist('tags')
            form = NoteForm(request.POST)
            new_note = form.save(commit=False)
            new_note.user_id = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=list_tags, user_id=request.user)  # WHERE name in []
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'project/notes.html', {"tags": tags, 'form': NoteForm(), 'error': err})

    return render(request, 'project/notes.html', {"tags": tags, 'form': NoteForm()})


@login_required
def show_notes(request):
    if request.method == 'GET':
        notes = Note.objects.all()
        return render(request, 'project/notes.html', {'back': '/', 'notes': notes})
    else:
        sort = request.POST['sort']
        print(sort)
        return render(request, 'project/notes.html', {'back': '/'})

@login_required
def set_done_note(request, note_id):
    Note.objects.filter(pk=note_id, user_id=request.user).update(done=True)
    return redirect('main')


@login_required
def delete_note(request, note_id):
    note = Note.objects.get(pk=note_id, user_id=request.user)
    note.delete()
    return redirect('main')

@login_required
def edit_note(request, note_id):
    note = Note.objects.get(pk=note_id, user_id=request.user)
    tags = Tag.objects.filter(user_id=request.user).all()
    if request.method == 'POST':
        try:
            list_tags = request.POST.getlist('tags')
            form = NoteForm(request.POST, instance=note)
            new_note = form.save(commit=False)
            new_note.user_id = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=list_tags, user_id=request.user)
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)
            return redirect(to='main')
        except ValueError as err:
            return render(request, 'project/notes.html', {"tags": tags, 'form': NoteForm(), 'error': err})

    return render(request, 'project/notes.html', {"tags": tags, 'form': NoteForm(instance=note)})

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

