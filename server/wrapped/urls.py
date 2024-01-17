from django.urls import path
from .views import fetch_goodreads_data, validate_users

urlpatterns = [
    path('/getreadingdetails', fetch_goodreads_data, name='Get Reading Wrapped Details'),
    path('/validateID', validate_users, name='Validate User ID')
]