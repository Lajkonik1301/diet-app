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
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Surrname'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'height', 'weight']

class GoalUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['goal_weight', 'caloric_intake', 'protein_intake', 'fat_intake', 'carbs_intake']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['goal_weight'].widget.attrs.update({'placeholder': 'Target weight (kg)'})
        self.fields['caloric_intake'].widget.attrs.update({'placeholder': 'Calories/day'})
        self.fields['protein_intake'].widget.attrs.update({'placeholder': 'Protein (g)'})
        self.fields['fat_intake'].widget.attrs.update({'placeholder': 'Fat (g)'})
        self.fields['carbs_intake'].widget.attrs.update({'placeholder': 'Carbs (g)'})

