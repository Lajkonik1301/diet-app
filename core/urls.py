from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('main/', views.main, name='main'),
    path('delete_meal/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_goals/', views.edit_goals, name='edit_goals'),
    path('statistics/', views.statistics, name='statistics'),
    path('history/', views.history, name='history'),
    path('recipes/', views.recipe_list, name='recipes'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    
]
