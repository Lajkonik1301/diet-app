from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from core.models import Meal

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
        date = request.POST.get("date")
        meal_type = request.POST.get("meal-type")
        protein = request.POST.get("protein")
        fat = request.POST.get("fat")
        carbs = request.POST.get("carbs")

        Meal.objects.create(
            user=request.user,
            name=name,
            calories=calories,
            date=date,
            meal_type=meal_type,
            protein=protein,
            fat=fat,
            carbs=carbs
        )
        return redirect("main")  # po dodaniu posiłku odśwież stronę
    
    return render(request, "core/main.html")

def recipes(request):
    return render(request, 'core/recipes.html')

def profile(request):
    return render(request, 'core/profile.html')

def statistics(request):
    return render(request, 'core/statistics.html')

def history(request):
    return render(request, 'core/history.html')