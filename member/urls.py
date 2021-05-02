from django.conf.urls import include, url
from member.views import dashboard, register
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.models import User
from django.views.generic import ListView


urlpatterns = [
    path('list/', ListView.as_view(model=User), name='user_list'),
    path('dashboard/', dashboard, name="dashboard"),
    path('register/', register, name="register"),
    # path('login/', auth_views.LoginView.as_view()),
    path('', include("django.contrib.auth.urls")),
]
