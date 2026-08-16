from django.urls import path
from .auth_router import auth_router
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tracks/', views.tracks, name='tracks'),
    path('accounts/login/', views.team_login, name='team_login'),
    path('team-dashboard/', views.participant_dashboard, name='dashboard'),
    path('dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/teams/', views.admin_teams, name='admin_teams'),
    path('admin-panel/teams/toggle-offline/<str:team_code>/', views.admin_toggle_offline_registration, name='admin_toggle_offline_registration'),
    path('admin-panel/marks/', views.admin_marks, name='admin_marks'),
    path('admin-panel/announcements/', views.admin_announcements, name='admin_announcements'),
    path('admin-panel/tracks/', views.admin_tracks, name='admin_tracks'),
    path("auth/router/", auth_router, name="auth_router"),
    path("oc-dashboard/announcements/delete/<int:announcement_id>/",views.delete_announcement,name="delete_announcement",),
    path('<str:page>/', views.information, name='information'),
]