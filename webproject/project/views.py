import io
import os

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import EmailValidator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from .models import Tag, Note, User, Files, AddressBook, Phones, Emails
from .forms import TagForm, NoteForm, ABForm

# Create your views here.
from .validation_ab import Phone, Birthday, Email, DateIsNotValid, DateVeryBig, items_ab, EmptyName
from .files_libs import *
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

items_note = ['Sort by ascending date', 'Sort by descending date', 'Sort tags']
sorted_news = []
currency = []
filters_for_news = ['Sort by ascending news', 'Sort by descending news']


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
    return render(request, 'project/index.html', {"notes": notes})


@login_required
def detail_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user_id=request.user)
    note.tag_list = ', '.join([str(name) for name in note.tags.all()])
    return render(request, 'project/detail_note.html', {"note": note})


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
            print('1')
            form = NoteForm(request.POST)
            print('1')
            new_note = form.save(commit=False)
            new_note.user_id = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=list_tags, user_id=request.user)  # WHERE name in []
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)
            return redirect(to='show_notes')
        except ValueError as err:
            return render(request, 'project/add_note.html', {"tags": tags, 'form': NoteForm(), 'error': err})

    return render(request, 'project/add_note.html', {"tags": tags, 'form': NoteForm()})


@login_required
def show_notes(request):
    global items_note
    notes = []
    if request.user.is_authenticated:
        notes = Note.objects.filter(user_id=request.user).all()
    return render(request, 'project/show_note.html', {"notes": notes, 'items': items_note})


@login_required
def set_done_note(request, note_id):
    Note.objects.filter(pk=note_id, user_id=request.user).update(done=True)
    return redirect('show_notes')


@login_required
def delete_note(request, note_id):
    note = Note.objects.get(pk=note_id, user_id=request.user)
    note.delete()
    return redirect('show_notes')


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
            return render(request, 'project/add_note.html', {"tags": tags, 'form': NoteForm(), 'error': err})

    return render(request, 'project/add_note.html', {"tags": tags, 'form': NoteForm(instance=note)})


@login_required
@csrf_protect
def filter_note(request, filter):
    global items_note
    print('1')
    notes = []
    filt = filter
    if request.method == 'GET':
        if filter == 'Sort tags':
            notes = Note.objects.filter(user_id=request.user).all().order_by('tags').values()
        elif filter == 'Sort by ascending date':
            notes = Note.objects.filter(user_id=request.user).all().order_by('-created').values()
        elif filter == 'Sort by descending date':
            notes = Note.objects.filter(user_id=request.user).all().order_by('created').values()
        else:
            search_value = request.GET.get('search_key')
            note = Note.objects.filter(
                Q(user_id=request.user, tags=search_value) | Q(user_id=request.user, name=search_value))
            notes = list(note)
        return render(request, 'project/show_note.html', {'notes': notes, 'items': items_note, 'filt': filt})


@csrf_exempt
@login_required
def add_contact(request):
    form = ABForm(request.POST)
    if request.method == 'POST':
        try:
            name = request.POST['fullname']
            if not name:
                raise  EmptyName
            phone = request.POST['phone']
            if phone:
                phone = Phone(phone).value
            birthday = request.POST['dob']
            if birthday:
                birthday = Birthday(birthday).value
                if birthday > datetime.now():
                    print('12')
                    raise DateVeryBig
            email = request.POST['email']
            if email:
                # email = Email(email).value
                email_validator = EmailValidator()
                email_validator(email)
            address = request.POST['address']
            storage = messages.get_messages(request)
            storage.used = True
            ab_phone = AddressBook.objects.filter(user_id=request.user, phones__phone_number=phone)
            ab_email = AddressBook.objects.filter(user_id=request.user, emails__mail=email)
            if ab_phone:
                messages.warning(request, 'This number already used')
                return render(request, 'project/contact_add.html', {'form': form})
            if ab_email:
                messages.warning(request, 'This address already used')
                return render(request, 'project/contact_add.html', {'form': form})
            contact = AddressBook(user_id=request.user, name=name)
            if birthday:
                contact.birthday = birthday
            if address:
                contact.address = address
            contact.save()
            if phone:
                new_phone = Phones(contact_id=contact.id, phone_number=phone, user_id=request.user.id)
                new_phone.save()
            if email:
                new_email = Emails(contact_id=contact.id, mail=email, user_id=request.user.id)
                new_email.save()
        except ValidationError:
            messages.warning(request, 'Email is not valid.')
            return render(request, 'project/contact_add.html', {'form': form})
        except EmptyName:
            messages.warning(request, 'Name cannot be empty')
            return render(request, 'project/contact_add.html', {'form': form})
        except ValueError:
            messages.warning(request, 'Invalid phone try 10 or 12 numbers')
            return render(request, 'project/contact_add.html', {'form': form})
        except DateIsNotValid:
            messages.warning(request, 'Invalid birthday, try: year-month-day')
            return render(request, 'project/contact_add.html', {'form': form})
        except AttributeError:
            messages.warning(request, 'Invalid email, try: symbols(,.@ a-z 0-9)')
            return render(request, 'project/contact_add.html', {'form': form})
        except DateVeryBig:
            messages.warning(request, 'This date bigger than present date')
            return render(request, 'project/contact_add.html', {'form': form})
        return redirect('show_contacts')
    else:
        return render(request, 'project/contact_add.html', {'form': form})


@csrf_exempt
@login_required
def edit_ab(request, ab_id):
    contact = AddressBook.objects.get(id=ab_id, user_id=request.user)
    form = ABForm(request.POST)
    if request.method == 'POST':
        try:
            name = request.POST['fullname']
            birthday = Birthday(request.POST['dob']).value
            if birthday > datetime.now():
                raise DateVeryBig
            address = request.POST['address']
            contact.name, contact.birthday, contact.address = name, birthday, address
            contact.save()
            storage = messages.get_messages(request)
            storage.used = True
            return redirect('show_contacts')
        except ValueError:
            messages.warning(request, 'Invalid phone try 10 or 12 numbers')
            return render(request, 'project/contact_edit.html', {'contact': contact, 'form': form})
        except DateIsNotValid:
            messages.warning(request, 'Invalid birthday, try: year-month-day')
            return render(request, 'project/contact_edit.html', {'contact': contact, 'form': form})
        except AttributeError:
            messages.warning(request, 'Invalid email, try: symbols(,.@ a-z 0-9)')
            return render(request, 'project/contact_edit.html', {'contact': contact, 'form': form})
        except DateVeryBig:
            messages.warning(request, 'This date bigger than present date')
            return render(request, 'project/contact_edit.html', {'contact': contact, 'form': form})
    else:
        return render(request, 'project/contact_edit.html', {'contact': contact, 'form': form})


@csrf_exempt
@login_required
def phones_edit(request, ab_id):
    phones_list = Phones.objects.filter(user_id=request.user, contact_id=ab_id).all()
    contact = AddressBook.objects.filter(user_id=request.user, id=ab_id).first()
    form = ABForm(request.POST)
    if request.method == 'POST':
        phone_id = int(request.POST.get('subbutton'))
        new_phone = request.POST.get(f'phone-{phone_id}')
        print(phone_id, new_phone)
        if not new_phone:
            messages.warning(request, 'Phone number is empty.')
            return render(request, 'project/phones_edit.html', {'phones': phones_list, 'contact': contact, 'form': form})
        try:
            new_phone = Phone(new_phone).value
            print(new_phone)
        except ValueError:
            messages.warning(request, 'Phone number is not valid.')
            return render(request, 'project/phones_edit.html', {'phones': phones_list, 'contact': contact, 'form': form})
        dubl_phone = Phones.objects.filter(phone_number=new_phone).exclude(id=phone_id).first()
        if dubl_phone:
            messages.warning(request, 'Phone number is now exist.')
            return render(request, 'project/phones_edit.html', {'phones': phones_list, 'contact': contact, 'form': form})
        if phone_id:
            phone = Phones.objects.filter(id=phone_id).first()
            mss = 'modify'
        else:
            phone = Phones(user_id=request.user.id, contact_id=ab_id)
            mss = 'add'
        phone.phone_number = new_phone
        phone.save()
        messages.info(request, f'Phone number {phone.phone_number} {mss}')

    return render(request, 'project/phones_edit.html', {'phones': phones_list, 'contact': contact, 'form': form})


@csrf_exempt
@login_required
def emails_edit(request, ab_id):
    emails_list = Emails.objects.filter(user_id=request.user, contact_id=ab_id).all()
    contact = AddressBook.objects.filter(user_id=request.user, id=ab_id).first()
    form = ABForm(request.POST)
    if request.method == 'POST':
        email_id = int(request.POST.get('subbutton'))
        new_email = request.POST.get(f'email-{email_id}')
        if not new_email:
            messages.warning(request, 'Email is empty.')
            return render(request, 'project/emails_edit.html', {'emails': emails_list, 'contact': contact, 'form': form})
        try:
            # new_email = Email(new_email).value
            email_validator = EmailValidator()
            email_validator(new_email)
        except ValidationError:
            messages.warning(request, 'Email is not valid.')
            return render(request, 'project/emails_edit.html', {'emails': emails_list, 'contact': contact, 'form': form})
        except ValueError:
            messages.warning(request, 'Email is not valid.')
            return render(request, 'project/emails_edit.html', {'emails': emails_list, 'contact': contact, 'form': form})
        except AttributeError:
            messages.warning(request, 'Email is not valid.')
            return render(request, 'project/emails_edit.html', {'emails': emails_list, 'contact': contact, 'form': form})
        dubl_email = Emails.objects.filter(mail=new_email).exclude(id=email_id).first()
        if dubl_email:
            messages.warning(request, 'Email is now exist.')
            return render(request, 'project/emails_edit.html', {'emails': emails_list, 'contact': contact, 'form': form})
        if email_id:
            email = Emails.objects.filter(id=email_id).first()
            mss = 'modify'
        else:
            email = Emails(user_id=request.user.id, contact_id=ab_id)
            mss = 'add'
        email.mail = new_email
        email.save()
        messages.info(request, f'Email {email.mail} {mss}')

    return render(request, 'project/emails_edit.html', {'emails': emails_list, 'contact': contact, 'form': form})


@login_required
def phone_del(request, ph_id):
    phone = Phones.objects.filter(id=ph_id).first()
    del_phone = phone.phone_number
    phone.delete()
    messages.info(request, f'Phone number {del_phone} deleted')
    if request.method == 'GET':
        return redirect('show_contacts')


def email_del(request, em_id):
    email = Emails.objects.filter(id=em_id).first()
    del_email = email.mail
    email.delete()
    messages.info(request, f'Email {del_email} deleted')
    if request.method == 'GET':
        return redirect('show_contacts')


@login_required
def delete_ab(request, ab_id):
    contact = AddressBook.objects.filter(id=ab_id).first()
    contact.delete()
    if request.method == 'GET':
        return redirect('show_contacts')


@login_required
def show_addressbook(request):
    global items_ab
    contacts = AddressBook.objects.filter(user_id=request.user).all()
    if request.method == 'GET':
        return render(request, 'project/contacts.html', {'contacts': contacts, 'items': items_ab})
    return render(request, 'project/contacts.html')


@login_required
@csrf_protect
def filter_addressbook(request, filter):
    global items_ab
    contacts = []
    filt = filter
    if request.method == 'GET':
        if filter == 'Sort alphabetically':
            contacts = AddressBook.objects.filter(user_id=request.user).all().order_by('name').values()
        elif filter == 'Sort by ascending date':
            contacts = AddressBook.objects.filter(user_id=request.user).all().order_by('-birthday').values()
        elif filter == 'Sort by descending date':
            contacts = AddressBook.objects.filter(user_id=request.user).all().order_by('birthday').values()
        elif filter == 'search':
            search_value = request.GET.get('search_key')
            contact = AddressBook.objects.filter(
                Q(user_id=request.user, phones__phone_number__icontains=search_value) | Q(user_id=request.user,
                name__icontains=search_value) | Q(user_id=request.user, emails__mail__icontains=search_value))
            contacts = list(set(contact))
        elif filter == 'to_birthday':
            days_to_bd = int(request.GET.get('search_days'))
            all_contact = AddressBook.objects.filter(user_id=request.user).all()
            contacts = [contact for contact in all_contact if 0 <= days_to_birthdays(contact.birthday) <= days_to_bd]
        return render(request, 'project/contacts.html', {'contacts': contacts, 'items': items_ab, 'filt': filt})


@csrf_protect
@login_required
def search(request):
    global items_ab
    if request.method == 'POST':
        search_value = request.POST.get('search_key')
        print(search_value)
        contact = AddressBook.objects.filter(
            Q(user_id=request.user, phone=search_value) | Q(user_id=request.user, name=search_value))
        contacts = list(contact)
        return render(request, 'project/contacts.html', {'contacts': contacts, 'items': items_ab})
    else:
        return redirect(to='filter_addressbook')


@csrf_protect
@login_required
def days_to_birthday(request):
    global items_ab
    if request.method == 'POST':
        days_to_bd = int(request.POST.get('search_days'))
        # print(days_to_bd)
        contact = AddressBook.objects.filter(user_id=request.user).all()
        contacts = list(contact)
        print(contacts)
        return render(request, 'project/contacts.html', {'contacts': contacts, 'items': items_ab})
    else:
        return redirect(to='filter_addressbook')


@login_required
def parser(request):
    global sorted_news
    global currency
    # CURRENCY
    # https://https://finance.i.ua/
    currency = []
    parsing_error = False

    base_url = 'https://finance.i.ua/'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        content = soup.find('div', class_='widget-currency_cash').find('table',
                                                                       class_='table table-data -important').find_all(
            'tr')
    except AttributeError:
        parsing_error = True
    if not parsing_error:
        for element in content:
            result = {}
            try:
                currency_name = element.find('th').text
                result.update({"currency_name": currency_name})
                rate_el = element.find_all('span', class_='')
                rate = []
                for _ in rate_el:
                    rate.append(_.text)
                result.update({"buy": rate[0]})
                result.update({"sale": rate[1]})
                currency.append(result)
            except AttributeError:
                parsing_error = True

    # NEWS
    news = []

    # https://ua.korrespondent.net/
    parsing_error = False
    base_url = 'https://ua.korrespondent.net/'
    data_source = 'korrespondent.net'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        content = soup.find('div', class_='time-articles').find_all('div', class_='article')
    except AttributeError:
        parsing_error = True
    if not parsing_error:
        for element in content:
            result = {}
            try:
                if element['class'][0] == 'time-articles__date':
                    print('-------------------------------------------------')
                    break
            except KeyError:
                continue
            dtime = element.find('div', class_="article__time").text
            date_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                 int(dtime.split(":")[0]),
                                 int(dtime.split(":")[1]))
            result.update({"dtime": date_time})
            title = element.find('div', attrs={"class": "article__title"}).text
            result.update({"title": title})
            href = element.find('div', attrs={"class": "article__title"}).find('a').get('href')
            result.update({"href": href})
            result.update({"source": data_source})
            news.append(result)

    # https://news.liga.net/
    parsing_error = False
    base_url = 'https://news.liga.net/'
    data_source = 'liga.net'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        content = soup.find('div', id='all-news').find_all('div')
    except AttributeError:
        parsing_error = True
    if not parsing_error:
        for element in content:
            result = {}
            try:
                if element['class'][0] == 'time-divider':
                    break
            except KeyError:
                continue
            try:
                dtime = element.find('div', attrs={"class": "news-nth-time"}).text
            except AttributeError:
                continue
            date_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                 int(dtime.split(":")[0]),
                                 int(dtime.split(":")[1]))
            result.update({"dtime": date_time})
            title = element.find('a').text
            result.update({"title": title})
            href = element.find('a').get('href')
            result.update({"href": href})
            result.update({"source": data_source})
            news.append(result)

    # https://www.pravda.com.ua/news/
    parsing_error = False
    base_url = 'https://www.pravda.com.ua/news/'
    data_source = 'Українська правда'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        content = soup.find('div', class_='container_sub_news_list_wrapper mode1').find_all('div',
                                                                                            class_='article_news_list')
    except AttributeError:
        parsing_error = True

    if not parsing_error:
        for element in content:
            result = {}
            dtime = element.find('div', class_="article_time").text
            date_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                 int(dtime.split(":")[0]),
                                 int(dtime.split(":")[1]))
            result.update({"dtime": date_time})
            title = element.find('div', attrs={"class": "article_header"}).text
            result.update({"title": title})
            href = element.find('div', attrs={"class": "article_header"}).find('a').get('href')

            result.update({"href": 'https://www.pravda.com.ua' + href})
            result.update({"source": data_source})
            news.append(result)

    news = filter(lambda nn: nn['dtime'] <= datetime.now(), news)
    sorted_news = sorted(news, key=lambda d: d['dtime'])
    sorted_news.reverse()

    for el in sorted_news:

        for k, v in el.items():

            if k == 'dtime':
                try:
                    el.update({"dtime": v.strftime("%H:%M")})
                except:
                    print(k, v)

    return render(request, 'project/info.html', {"news": sorted_news, 'currency': currency})


@login_required
def view_files(request):
    all_files = Files.objects.filter(user_id=request.user).all()
    return render(request, 'project/files.html', {'gfiles': all_files, 'filt': ''})


@login_required
def filter_files(request, filt):
    all_files = Files.objects.filter(user_id=request.user, type=filt).all()
    return render(request, 'project/files.html', {'gfiles': all_files, 'filt': filt})


@login_required
def file_download(request, file_id):
    down_file = Files.objects.filter(user_id=request.user, id=file_id).first()
    fileid = down_file.up_id
    grequest = service.files().get_media(fileId=fileid)
    down_dir = DOWNLOAD_DIR / str(request.user)
    down_dir.mkdir(exist_ok=True, parents=True)
    filename = DOWNLOAD_DIR / str(request.user) / down_file.name
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, grequest)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    messages.info(request, f'File {down_file.name} downloaded')
    return redirect('view_files')


@login_required
def file_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        file = request.FILES['myfile']
        if os.path.exists(UPLOAD_DIR / file.name):
            os.remove(UPLOAD_DIR / file.name)
        fs = FileSystemStorage(UPLOAD_DIR)
        filename = fs.save(file.name, file)
        ext = get_extension(filename)
        filetype = file_type(ext)
        file_path = UPLOAD_DIR / filename
        file_metadata = {
            'name': filename,
            'parents': [GDRIVE_FOLDER_ID]
        }
        media = MediaFileUpload(file_path, resumable=True)
        r = service.files().create(body=file_metadata, media_body=media, fields='id, size, createdTime').execute()
        print(r)
        new_file = Files(user_id=request.user, name=filename)
        new_file.size = int(r['size'])
        new_file.type = filetype
        new_file.up_id = r['id']
        new_file.up_time = r['createdTime']
        new_file.save()
        messages.info(request, f'File {filename} uploaded')
        return redirect('view_files')
    return render(request, 'project/file_upload.html')


def about_us(request):
    return render(request, 'project/about_us.html')
