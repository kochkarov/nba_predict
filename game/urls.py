from django.urls import path, register_converter
from . import views, converters


register_converter(converters.DateConverter, 'yyyymmdd')

urlpatterns = [
    path('', views.index),
    path('<yyyymmdd:day>/', views.day_archive),
]
