# email_sf/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_emails, name='show_emails'),  # URL pattern for showing emails
]
