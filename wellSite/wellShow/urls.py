from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),      # "/" → starter page
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),

    # your existing API endpoints
    path('receive/', views.receive_record, name='receive'),
    path('create/', views.create_well, name='create'),
]