# forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from utilisateurs.models import Utilisateurs


# forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from utilisateurs.models import Utilisateurs

class PasswordChangeCustomForm(PasswordChangeForm):
    class Meta:
        model = Utilisateurs
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

from django import forms
from django.contrib.auth.hashers import make_password
from utilisateurs.models import Utilisateurs, Fonction

class UtilisateurmettreajourForm(forms.ModelForm):
    password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    fonction = forms.ModelChoiceField(queryset=Fonction.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Utilisateurs
        fields = ['nom_complet', 'email', 'fonction', 'password', 'profile_image']
        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            instance.password = make_password(password)

        if commit:
            instance.save()

        return instance



from django import forms
from django.contrib.auth.forms import UserCreationForm

class UtilisateursCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateurs
        fields = ['email', 'nom_complet', 'fonction', 'password1', 'password2', 'profile_image']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nom_complet': forms.TextInput(attrs={'class': 'form-control'}),
            'fonction': forms.Select(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


