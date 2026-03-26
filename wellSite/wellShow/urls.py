from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('receive', views.new_rec, name='receive')
]