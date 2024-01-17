from django.urls import path, include

urlpatterns = [
    path('wrapped/', include('wrapped.urls'))
]
