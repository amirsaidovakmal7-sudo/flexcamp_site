from django.urls import path
from . import views

urlpatterns = [
 path('', views.home_page),
 path('order', views.send_form),
]