from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

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


def main(request):
    return render(request, 'core/main.html')