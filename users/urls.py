from django.urls import path
from . import views

app_name = 'users'  # Define the namespace

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard_home'),  # Default view for logged-in user
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard_user'),
    path('test-twitter/', views.some_view, name='test_twitter'),
]