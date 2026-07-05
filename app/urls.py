from django.urls import path
from . import views

urlpatterns = [
 path('', views.home_page, name='home'),
 path('order', views.send_form, name='order'),
 path('create-comment', views.create_comment, name='create_comment'),

]