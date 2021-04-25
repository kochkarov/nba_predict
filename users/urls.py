from django.conf.urls import include, url
from users.views import dashboard, register

urlpatterns = [
    url('dashboard/', dashboard, name="dashboard"),
    url('register/', register, name="register"),
    url('', include("django.contrib.auth.urls")),
]
