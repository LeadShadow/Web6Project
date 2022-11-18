from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('add_tags/', views.tag, name='usertag'),
    path('notes/', views.note, name='notes'),
    path('show_note/', views.show_notes, name='show_note'),
    path('done_note/<int:note_id>', views.set_done_note, name='set_done_note'),
    path('delete/<int:note_id>', views.delete_note, name='delete_note'),
    path('show_notes', views.show_notes, name='show_notes'),
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('contact/', views.addressbook, name='contact'),
    path('contacts/edit/<int:ab_id>', views.edit_ab, name='edit_ab'),
    path('show_contacts/', views.show_addressbook, name='show_contacts'),
    path('contacts/delete/<int:ab_id>', views.delete_ab, name='delete_ab'),
    path('show_contacts/<str:filter>', views.filter_addressbook, name='filter_addressbook'),
    path('note_edit/<int:note_id>', views.edit_note, name='note_edit'),
    path('info_collector/', views.parser, name='parser'),
    path('detail_note/<int:note_id>', views.detail_note, name='detail_note'),
    path('files/', views.view_files, name='view_files'),
    path('files/filter/<str:filt>', views.filter_files, name='filter_files'),
    path('files/add/', views.file_upload, name='file_upload'),
    path('files/down/<int:file_id>', views.file_download, name='file_download'),

]
