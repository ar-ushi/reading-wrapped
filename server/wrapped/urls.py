from django.urls import path
from .views import fetch_goodreads_data, validate_users

urlpatterns = [
    path('yearlystats', fetch_goodreads_data, name='Yearly Reading Stats'),
    path('validateID', validate_users, name='Validate User ID')
]