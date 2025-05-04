from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        #pola tekstowe
        self.fields['username'].widget.attrs.update({'placeholder': 'Nazwa użytkownika'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Imię'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nazwisko'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Podaj hasło'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Powtórz hasło'})