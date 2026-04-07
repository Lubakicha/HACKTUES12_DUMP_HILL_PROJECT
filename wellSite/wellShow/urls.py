from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),      # "/" → starter page
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),

    # your existing API endpoints
    path('receive', views.receive_record, name='receive'),
    path('create/', views.create_well, name='create'),
    path('home/logout/', views.logout_view, name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('home/new_well/', views.create_well, name='well'),
    path('inbox/', views.inbox, name='inbox'),
    path('event/<int:event_id>/resolve/', views.resolve_event, name='resolve_event'),
    path('event/<int:event_id>/create/', views.create_well_from_event, name='create_well_from_event'),
    path('set-critical/', views.set_critical, name='set_critical'),
    path('check-alert/', views.check_alert),
    path('resolve-event/<int:event_id>/', views.resolve_event, name='resolve_event'),
]