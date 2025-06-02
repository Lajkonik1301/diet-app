from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileUpdateForm, GoalUpdateForm
from core.models import Meal
from .models import Recipe
from django.shortcuts import get_object_or_404, redirect
import json

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')  # Po zalogowaniu przekierowanie na stronę główną
    else:
        form = AuthenticationForm()

    form.fields['username'].widget.attrs.update({'placeholder': 'Nazwa użytkownika'})
    form.fields['password'].widget.attrs.update({'placeholder': 'Podaj hasło'})

    #schowanie errorów
    form.errors.clear()

    return render(request, 'core/index.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')  # Przekierowanie na stronę główną
    else:
        form = AuthenticationForm()
    return render(request, 'core/index.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Logowanie po rejestracji
            return redirect('main')  # Przekierowanie na stronę główną
    else:
        form = RegisterForm()

    #schowanie errorów
    form.errors.clear()

    return render(request, 'core/register_page.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') 

def main(request):
    if request.method == "POST":
        name = request.POST.get("meal-name")
        calories = request.POST.get("calories")
        date_input = request.POST.get("date")
        meal_type = request.POST.get("meal-type")
        protein = request.POST.get("protein")
        fat = request.POST.get("fat")
        carbs = request.POST.get("carbs")

        Meal.objects.create(
            user=request.user,
            name=name,
            calories=calories,
            date=date_input,
            meal_type=meal_type,
            protein=protein,
            fat=fat,
            carbs=carbs
        )
        return redirect("main") # po dodaniu posiłku odśwież stronę
    
    # Na sztywno cele dzienne spożycia
    goal_calories = 2200
    goal_protein = 100
    goal_fat = 70
    goal_carbs = 250

    # Obliczanie dziennego spożycia
    today = date.today()
    meals_today = Meal.objects.filter(user=request.user, date=today)

    total_calories = sum(meal.calories for meal in meals_today)
    remaining_calories = max(goal_calories - total_calories, 0)

    total_protein = sum(meal.protein for meal in meals_today)
    remaining_protein = max(goal_protein - total_protein, 0)

    total_fat = sum(meal.fat for meal in meals_today)
    remaining_fat = max(goal_fat - total_fat, 0)

    total_carbs = sum(meal.carbs for meal in meals_today)
    remaining_carbs = max(goal_carbs - total_carbs, 0)

    context = {
        "total_calories": total_calories,
        'remaining_calories': remaining_calories,
        "total_protein": total_protein,
        'remaining_protein': remaining_protein,
        "total_fat": total_fat,
        'remaining_fat': remaining_fat,
        "total_carbs": total_carbs,
        'remaining_carbs': remaining_carbs,
        "goal_calories": goal_calories,
        "goal_protein": goal_protein,
        "goal_fat": goal_fat,
        "goal_carbs": goal_carbs,
        "meals_today": meals_today,
    }

    return render(request, "core/main.html", context)

def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    meal.delete()
    return redirect('main')

def recipe_list(request):
    query = request.GET.get('q', '')
    # recipes = Recipe.objects.all()
    recipes = Recipe.objects.all()

    #if query:
    #    recipes = recipes.filter(name__icontains=query)

    paginator = Paginator(recipes, 9)  # 6 = 2 rzędy po 3
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/recipes.html', {'recipes': page_obj, 'recipes_count': recipes.count()})
    #return render(request, 'core/recipes.html', {'recipes': page_obj})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        recipe = Recipe(
            user=request.user,
            name=request.POST.get('name'),
            instructions=request.POST.get('instructions'),
            calories=int(request.POST.get('calories')),
            protein=int(request.POST.get('protein')),
            fat=int(request.POST.get('fat')),
            carbs=int(request.POST.get('carbs')),
            meal_type=request.POST.get('meal_type'),
            prep_time=int(request.POST.get('prep_time')),
        )
        recipe.save()
        return redirect('recipes')
    return render(request, 'core/add_recipe.html')

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'core/recipe_detail.html', {'recipe': recipe})

def profile(request):
    return render(request, 'core/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})
    
@login_required
def edit_goals(request):
    user = request.user

    if request.method == 'POST':
        form = GoalUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = GoalUpdateForm(instance=user)

    return render(request, 'core/edit_goals.html', {'form': form})

@login_required
def statistics(request):
    today = date.today()
    start_date = today - timedelta(days=6)

    meals = Meal.objects.filter(user=request.user, date__range=[start_date, today])

    daily_data = {}
    for day in range(7):
        day_date = start_date + timedelta(days=day)
        daily_data[day_date] = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}

    for meal in meals:
        daily = daily_data[meal.date]
        daily['calories'] += meal.calories
        daily['protein'] += meal.protein
        daily['fat'] += meal.fat
        daily['carbs'] += meal.carbs

    dates = [d.strftime('%Y-%m-%d') for d in daily_data.keys()]
    calories = [daily_data[d]['calories'] for d in daily_data.keys()]
    protein = [daily_data[d]['protein'] for d in daily_data.keys()]
    fat = [daily_data[d]['fat'] for d in daily_data.keys()]
    carbs = [daily_data[d]['carbs'] for d in daily_data.keys()]

    user = request.user
    goal_calories = user.caloric_intake or 2200
    goal_protein = user.protein_intake or 100
    goal_fat = user.fat_intake or 70
    goal_carbs = user.carbs_intake or 250

    context = {
        'dates': json.dumps(dates),
        'calories': json.dumps(calories),
        'protein': json.dumps(protein),
        'fat': json.dumps(fat),
        'carbs': json.dumps(carbs),
        'goal_calories': json.dumps(goal_calories),
        'goal_protein': json.dumps(goal_protein),
        'goal_fat': json.dumps(goal_fat),
        'goal_carbs': json.dumps(goal_carbs),
    }
    return render(request, 'core/statistics.html', context)

@login_required
def history(request):
    today = date.today()
    start_date = today - timedelta(days=6)  # 7 dni łącznie
    
    meals_last_7_days = Meal.objects.filter(
        user=request.user,
        date__range=[start_date, today]
    ).order_by('date')

    # Grupowanie posiłków po datach
    from collections import defaultdict
    meals_by_date = defaultdict(list)
    for meal in meals_last_7_days:
        meals_by_date[meal.date].append(meal)

    # Posortowana lista krotek (data, lista posiłków)
    sorted_meals = sorted(meals_by_date.items(), key=lambda x: x[0], reverse=True)

    context = {
        "meals_by_date": sorted_meals,
    }
    return render(request, "core/history.html", context)