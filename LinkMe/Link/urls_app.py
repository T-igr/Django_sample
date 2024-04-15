

from django.urls import path, re_path
from . import views

urlpatterns = [

    path('', views.master_list, name='master_list'),
    path('link/<slug:user_id>/', views.link, name='link'),
    path('calendar/', views.calendar, name='calendar'),
    path('book/', views.book, name='book'),
    path('test/', views.book_appointment, name='book_appointment'),

]