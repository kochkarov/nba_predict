from django.urls import path
from django.contrib.auth.models import User
from django.views.generic import ListView

urlpatterns = [
    path('', ListView.as_view(model=User), name='user_list'),
]
