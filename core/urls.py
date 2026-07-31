from django.urls import path
from .auth_router import auth_router
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tracks/', views.tracks, name='tracks'),
    path('accounts/login/', views.team_login, name='team_login'),
    path('team-dashboard/', views.team_dashboard_static, name='team_dashboard_static'),
    path('dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/teams/', views.admin_teams, name='admin_teams'),
    path('admin-panel/marks/', views.admin_marks, name='admin_marks'),
    path('admin-panel/announcements/', views.admin_announcements, name='admin_announcements'),
    path('admin-panel/tracks/', views.admin_tracks, name='admin_tracks'),
    path('admin-panel/sponsors/', views.admin_sponsors, name='admin_sponsors'),
    path('registration/', views.registration_index, name='registration_index'),
    path('registration/event-hub/', views.registration_event_hub, name='registration_event_hub'),
    path("auth/router/", auth_router, name="auth_router"),
    path("access-denied/", views.access_denied, name="access_denied"),
    path('<str:page>/', views.information, name='information'),
]