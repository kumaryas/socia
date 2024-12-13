from django.urls import path
from . import views

urlpatterns = [
    #path('', views.get_recent_tweet, name='dashboard'),  # Dashboard page showing recent tweet
    path('', views.dashboard, name='dashboard'),
]
