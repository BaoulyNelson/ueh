from django import forms
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from datetime import datetime


class FormulaireCreationUtilisateur(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse email")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2')


class FormulaireAuthentificationPersonnalise(AuthenticationForm):
    username = forms.CharField(
        label="Nom d’utilisateur ou Email",
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class FormulaireMiseAJourUtilisateur(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



def validate_year(value):
    current_year = datetime.now().year  # Récupérer l'année actuelle
    if value < 1900 or value > current_year:  # Par exemple, ne permet pas les années inférieures à 1900 ou supérieures à l'année actuelle
        raise ValidationError(f"L'année doit être comprise entre 1900 et {current_year}.")



        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nom', 'prenom', 'email', 'telephone', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'placeholder': 'Nom',
                'class': 'form-control',
            }),
            'prenom': forms.TextInput(attrs={
                'placeholder': 'Prénom',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Votre adresse email',
                'class': 'form-control',
            }),
            'telephone': forms.TextInput(attrs={
                'placeholder': 'Téléphone',
                'class': 'form-control',
            }),
            'sujet': forms.TextInput(attrs={
                'placeholder': 'Sujet de votre message',
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Votre message ici...',
                'class': 'form-control',
                'rows': 5,
            }),
        }

class DocumentSearchForm(forms.Form):
    annee = forms.ChoiceField(
        choices=[],  
        required=True,
        label="Quelle Année ?",
        widget=forms.Select(attrs={'id': 'annee', 'class': 'form-select'})
    )
    matricule = forms.CharField(
        required=True,
        label="Matricule",
        widget=forms.TextInput(attrs={'id': 'matricule', 'class': 'form-control'})
    )
    nom = forms.CharField(
        required=True,
        label="Nom de Famille",
        widget=forms.TextInput(attrs={'id': 'nom', 'class': 'form-control'})
    )
    prenom = forms.CharField(
        required=True,
        label="Prénom",
        widget=forms.TextInput(attrs={'id': 'prenom', 'class': 'form-control'})
    )
    telephone = forms.CharField(
        required=True,
        label="Téléphone",
        widget=forms.TextInput(attrs={'id': 'telephone', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        years = kwargs.pop('years', [])  
        super().__init__(*args, **kwargs)
        self.fields['annee'].choices = [('', 'Sélectionnez une année')] + [(year, year) for year in years]



class BaccalaureatForm(forms.Form):
    matricule = forms.CharField(
        label="Numéro d'ordre",
        max_length=10,   # côté Django
        min_length=10,   # côté Django (optionnel si tu veux exactement 10)
        widget=forms.TextInput(attrs={
            'placeholder': 'Matricule ici',
            'class': 'matricule-input',
            'maxlength': '10',        # côté HTML : impossible de taper plus de 10
            'pattern': '[0-9]{10}',   # côté HTML : validation → seulement 10 chiffres
            'title': 'Entrez exactement 10 chiffres'  # info bulle
        })
    )
