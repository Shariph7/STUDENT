from django.contrib import admin
from django.urls import path
from Home import views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name='index'),
    path("login", views.login, name='login'),
    path("student", views.student, name='student'),
    path("logout", views.logout, name='logout'),
    path("book_event", views.book_event, name="book_event"),
    path('cancel_event', views.cancel_event, name='cancel_event')
]