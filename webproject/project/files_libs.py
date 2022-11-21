from pathlib import Path
from datetime import datetime, date

from django.conf import settings
from django.http import request
from django.views.decorators.csrf import csrf_protect
from google.oauth2 import service_account
from googleapiclient.discovery import build


REGISTER_EXTENSIONS = {'Images': ['JPEG', 'PNG', 'JPG', 'SVG', 'GIF', 'ICO'],
                       'Audio': ['MP3', 'OGG', 'WAV', 'AMR', 'FLAC', 'WMA'],
                       'Video': ['AVI', 'MP4', 'MOV', 'MKV', 'WMV'],
                       'Documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'RTF'],
                       'Programs': ['BAT', 'CMD', 'EXE', 'C', 'CPP', 'JS', 'PY', 'VBS'],
                       'Archives': ['ZIP', 'GZ', 'TAR', 'RAR', '7Z', 'ARJ']
                       }

UPLOAD_DIR = Path('project/temp/')
DOWNLOAD_DIR = Path('project/download/')

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'web6project.json'

GDRIVE_FOLDER_ID = '1RdYoVP5lycHHNtraHrOPz9KkFoagOLIz'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def file_type(ext: str) -> str:
    for key, list_value in REGISTER_EXTENSIONS.items():
        if ext in list_value:
            return key
    else:
        return 'Others'


def days_to_birthdays(birthday) -> int:
    if birthday is None:
        return -1
    this_day = datetime.today().date()
    birthday_day = date(this_day.year, birthday.month, birthday.day)
    if birthday_day < this_day:
        birthday_day = date(this_day.year + 1, birthday.month, birthday.day)
    return int((birthday_day - this_day).days)