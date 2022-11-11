from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='usertag'),
    path('note/', views.note, name='note'),
    path('detail/<int:note_id>', views.detail_note, name='detail'),
    path('done_note/<int:note_id>', views.set_done_note, name='set_done_note'),
    path('delete/<int:note_id>', views.delete_note, name='delete_note'),
    path('show_notes', views.show_notes, name='show_notes'),
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('addressbook/', views.addressbook, name='addressbook'),
    path('edit_ab/<int:ab_id>', views.edit_ab, name='edit_ab'),
    path('show_addressbook/', views.show_addressbook, name='show_addressbook'),
    path('delete_ab/<int:ab_id>', views.delete_ab, name='delete_ab'),
    path('done_ab/<int:ab_id>', views.set_done_ab, name='set_done_ab')
]
