from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from core.models import Meal
from .models import Recipe
from django.shortcuts import get_object_or_404, redirect

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

    paginator = Paginator(recipes, 6)  # 6 = 2 rzędy po 3
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
            description=request.POST.get('description'),
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
    # Tymczasowy placeholder do czasu implementacji
    return render(request, 'core/recipe_detail.html', {'recipe_id': recipe_id})

def profile(request):
    return render(request, 'core/profile.html')

def edit_profile(request):
   
    return render(request, 'core/edit_profile.html')
    
def edit_goals(request):
    
    return render(request, 'core/edit_goals.html')

def statistics(request):
    return render(request, 'core/statistics.html')

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