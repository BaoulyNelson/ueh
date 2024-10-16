from django import forms
from .models import Departement, Commune, Profil, Adresse, Etude,Entite
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from datetime import datetime

def filtrer_communes_par_departement(form_instance, departement_field, commune_field):
    # Vérifie si le champ département est dans les données du formulaire
    if departement_field in form_instance.data:
        try:
            departement_id = int(form_instance.data.get(departement_field))
            form_instance.fields[commune_field].queryset = Commune.objects.filter(
                departement_id=departement_id).order_by('nom')
        except (ValueError, TypeError):
            form_instance.fields[commune_field].queryset = Commune.objects.none(
            )
    elif form_instance.instance.pk:  # Lors de l'édition d'une instance existante
        if hasattr(form_instance.instance, 'departement'):
            form_instance.fields[commune_field].queryset = form_instance.instance.departement.communes.order_by(
                'nom')
        else:
            form_instance.fields[commune_field].queryset = Commune.objects.none(
            )
    else:
        # Si aucun département n'est sélectionné
        form_instance.fields[commune_field].queryset = Commune.objects.none()


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


class FormulaireMiseAJourProfil(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['adresse', 'etudes']


class FormulaireAdresse(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = ['no', 'adresse', 'departement', 'commune']

        widgets = {
            'no': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'departement': forms.Select(attrs={'class': 'form-control'}),
            'commune': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filtrer_communes_par_departement(self, 'departement', 'commune')


def validate_year(value):
    current_year = datetime.now().year  # Récupérer l'année actuelle
    if value < 1900 or value > current_year:  # Par exemple, ne permet pas les années inférieures à 1900 ou supérieures à l'année actuelle
        raise ValidationError(f"L'année doit être comprise entre 1900 et {current_year}.")

class FormulaireEtude(forms.ModelForm):
    class Meta:
        model = Etude
        fields = ['niveau', 'institution', 'annee', 'departement']

        widgets = {
            'niveau': forms.Select(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'departement': forms.Select(attrs={'class': 'form-control'}),
        }

    # Ajouter le validateur à l'année
    annee = forms.IntegerField(validators=[validate_year], widget=forms.NumberInput(attrs={'class': 'form-control'}))

class FormulaireEntite(forms.ModelForm):
    # Champ de sélection pour choisir une nouvelle entité
    nouvelle_entite = forms.ModelChoiceField(
        queryset=Entite.objects.all(),  # Toutes les entités disponibles
        widget=forms.Select(attrs={'class': 'form-control'}),  # Liste déroulante stylée
        label="Choisir une nouvelle entité",
        required=True
    )

    class Meta:
        model = Entite
        fields = []  # Pas besoin d'inclure d'autres champs ici si ce n'est pas nécessaire