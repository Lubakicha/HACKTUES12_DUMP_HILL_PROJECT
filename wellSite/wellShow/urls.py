from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('receive/', views.receive_record, name='receive'),
    path('create/', views.create_well, name='create'),
]