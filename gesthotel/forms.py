from django import forms
from .models import TypeChambre, Chambre, Client, AffectationChambre


class TypeChambreForm(forms.ModelForm):
    class Meta:
        model = TypeChambre
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prix_nuit': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix_heure': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        fields = '__all__'
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'type_chambre': forms.Select(attrs={'class': 'form-control'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
            'nombre_lits': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'nom_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AffectationChambreForm(forms.ModelForm):
    class Meta:
        model = AffectationChambre
        fields = '__all__'
        widgets = {
            'chambre': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'client_anonyme': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



from django import forms
from .models import PiecesJointes

class PiecesJointesForm(forms.ModelForm):
    class Meta:
        model = PiecesJointes
        fields = ['titre', 'contenu', 'piece_jointe']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control'}),
            'piece_jointe': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['nom_notification', 'date_notification', 'heure_notification']
        widgets = {
            'nom_notification': forms.TextInput(attrs={'class': 'form-control'}),
            'date_notification': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_notification': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
