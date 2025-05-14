from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('main/', views.main, name='main'),
    path('logout/', views.logout_view, name='logout'),
    path('recipes/', views.recipes, name='recipes'),
    path('profile/', views.profile, name='profile'),
    path('statistics/', views.statistics, name='statistics'),
    path('history/', views.history, name='history'),
]
