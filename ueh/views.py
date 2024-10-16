# Pas de modification ici, ce sont des mots-clés Django
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# Assurez-vous que le chemin est correct (pas de changement pour "Commune" si c'est un modèle)
from .models import Commune, Etude, Departement, Adresse, Entite,Bachelier
from django.contrib import messages  # Pas de modification ici
from django.http import HttpResponse
from datetime import datetime
# Créez vos vues ici.
from django.http import JsonResponse  # Pas de modification ici
# Mots-clés Django, restent inchangés
from django.contrib.auth import login, authenticate, logout
# Traduction des formulaires personnalisés
from .forms import FormulaireCreationUtilisateur, FormulaireAuthentificationPersonnalise
from django.shortcuts import get_object_or_404
from django.http import Http404
import json
from django.http import HttpResponseNotFound

from django.contrib.auth.decorators import login_required  # Pas de modification ici
# Traduction des noms de formulaires
from .forms import FormulaireMiseAJourUtilisateur, FormulaireAdresse, FormulaireEtude, FormulaireEntite
import csv  # Pas de modification ici
from django.core.management.base import BaseCommand  # Pas de modification ici
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64

def accueil(request):
    return render(request, 'index.html')

def connexion(request):
    if request.method == 'POST':
        formulaire = FormulaireAuthentificationPersonnalise(
            request, data=request.POST)
        if formulaire.is_valid():
            login(request, formulaire.get_user())
            messages.success(request, 'Connexion réussie ! Bienvenue.')
            return redirect('accueil')  # Redirection vers la page d'accueil
        else:
            messages.error(
                request, 'Identifiants invalides. Veuillez réessayer.')
    else:
        formulaire = FormulaireAuthentificationPersonnalise()

    return render(request, 'comptes/connexion.html', {'formulaire': formulaire})

def inscription(request):
    if request.method == 'POST':
        formulaire = FormulaireCreationUtilisateur(request.POST)
        if formulaire.is_valid():
            utilisateur = formulaire.save()

            # Utilisez authenticate pour authentifier l'utilisateur avec email ou nom d'utilisateur
            utilisateur = authenticate(
                request, username=utilisateur.username, password=formulaire.cleaned_data.get('password1'))

            if utilisateur is not None:
                # Connexion sans besoin de spécifier le backend après authenticate
                login(request, utilisateur)

                # Message de succès
                messages.success(request, 'Inscription réussie ! Bienvenue.')
                # Redirection vers la page d'accueil
                return redirect('accueil')
            else:
                messages.error(
                    request, "Impossible de vous authentifier après l'inscription.")
        else:
            # Message d'erreur en cas de formulaire invalide
            messages.error(request, 'Veuillez corriger les erreurs ci-dessus.')
    else:
        formulaire = FormulaireCreationUtilisateur()

    return render(request, 'comptes/inscription.html', {'formulaire': formulaire})

@login_required
def ajouter_objet(request, objet_type):
    objets_mapping = {
        'etude': (FormulaireEtude, 'comptes/ajouter_etude.html'),
        'adresse': (FormulaireAdresse, 'comptes/ajouter_adresse.html'),
    }

    if objet_type not in objets_mapping:
        raise Http404("Type d'objet invalide.")

    formulaire_classe, template = objets_mapping[objet_type]

    if request.method == 'POST':
        formulaire = formulaire_classe(request.POST)
        if formulaire.is_valid():
            objet = formulaire.save(commit=False)
            objet.utilisateur = request.user
            objet.save()
            messages.success(
                request, f'{objet_type.capitalize()} ajouté(e) avec succès !')
            return redirect('details', type='utilisateur', id=request.user.id)  # Redirection vers le profil utilisateur

        else:
            messages.error(
                request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        formulaire = formulaire_classe()

    return render(request, template, {'formulaire': formulaire})

# @login_required
# def modifier_objet(request, objet_type, objet_id):
#     # Mapping entre le type d'objet et son modèle, son formulaire, et son template
#     objets_mapping = {
#         'entite': (Entite, FormulaireEntite, 'comptes/mise_a_jour_entite.html'),
#         'etude': (Etude, FormulaireEtude, 'comptes/mise_a_jour_etude.html'),
#         'adresse': (Adresse, FormulaireAdresse, 'comptes/mise_a_jour_adresse.html')
#     }

#     # Vérifier si le type d'objet est valide
#     if objet_type not in objets_mapping:
#         raise Http404("Type d'objet invalide.")

#     # Récupérer le modèle, le formulaire et le template correspondants
#     objet_classe, formulaire_classe, template = objets_mapping[objet_type]

#     # Récupérer l'objet et vérifier qu'il appartient à l'utilisateur (sauf pour les entités)
#     if objet_type == 'entite':
#         objet = get_object_or_404(objet_classe, id=objet_id)
#     else:
#         # Pour les autres objets, vérifier qu'ils appartiennent à l'utilisateur
#         objet = get_object_or_404(objet_classe, id=objet_id, utilisateur=request.user)

#     # Gérer le formulaire de modification
#     if request.method == 'POST':
#         formulaire = formulaire_classe(request.POST, instance=objet)
#         if formulaire.is_valid():
#             # Sauvegarder le formulaire
#             formulaire.save()

#             # Message de succès après la sauvegarde
#             messages.success(request, f'{objet_type.capitalize()} modifié(e) avec succès !')

#             # Redirection selon le type d'objet modifié
#             if objet_type == 'entite':
#                 return redirect('details', type='entite', id=objet_id)
#             else:
#                 return redirect('details', type='utilisateur', id=request.user.id)

#     else:
#         formulaire = formulaire_classe(instance=objet)

#     # Rendre la page avec le formulaire et passer explicitement l'objet dans le contexte
#     return render(request, template, {
#         'formulaire': formulaire,
#         'objet': objet,  # Passer l'objet ici pour le template
#         'objet_type': objet_type  # Optionnel pour savoir quel type d'objet tu traites
#     })

@login_required
def modifier_objet(request, objet_type, objet_id):
    # Mapping des types d'objets vers leurs modèles, formulaires et templates
    objets_mapping = {
        'entite': (Entite, FormulaireEntite, 'comptes/mise_a_jour_entite.html'),
        'etude': (Etude, FormulaireEtude, 'comptes/mise_a_jour_etude.html'),
        'adresse': (Adresse, FormulaireAdresse, 'comptes/mise_a_jour_adresse.html')
    }

    # Vérification si le type d'objet est valide
    if objet_type not in objets_mapping:
        raise Http404("Type d'objet invalide.")

    # Récupérer le modèle, le formulaire et le template correspondant
    objet_classe, formulaire_classe, template = objets_mapping[objet_type]

    # Récupérer l'objet à modifier
    if objet_type == 'entite':
        objet = get_object_or_404(objet_classe, id=objet_id)
    else:
        objet = get_object_or_404(objet_classe, id=objet_id, utilisateur=request.user)

    # Récupérer toutes les entités pour la liste déroulante
    entites = Entite.objects.all()

    if request.method == 'POST':
        # Vérifier si une nouvelle entité a été sélectionnée dans le formulaire
        nouvelle_entite_id = request.POST.get('nouvelle_entite')
        
        if nouvelle_entite_id:
            # Associer la nouvelle entité à l'objet si elle est valide
            nouvelle_entite = get_object_or_404(Entite, id=nouvelle_entite_id)
            objet.entite = nouvelle_entite  # Modifier l'entité associée à l'objet

        # Remplir le formulaire avec les données postées et l'instance actuelle
        formulaire = formulaire_classe(request.POST, instance=objet)
        
        # Si le formulaire est valide, sauvegarder l'objet
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, f'{objet_type.capitalize()} modifié(e) avec succès !')

            # Redirection après mise à jour : entité ou utilisateur
            if objet_type == 'entite':
                return redirect('details', type='entite', id=objet_id)
            else:
                return redirect('details', type='utilisateur', id=request.user.id)

    else:
        # Pré-remplir le formulaire avec les données actuelles de l'objet
        formulaire = formulaire_classe(instance=objet)

    # Rendre la page de modification avec le formulaire
    return render(request, template, {
        'formulaire': formulaire,
        'objet': objet,
        'objet_type': objet_type,
        'entites': entites
    })

@login_required
def supprimer_objet(request, objet_type, objet_id):
    # Mapping entre le type d'objet et son modèle et son template
    objets_mapping = {
        'entite': (Entite, 'comptes/supprimer_entite.html'),
        'etude': (Etude, 'comptes/supprimer_etude.html'),
        'adresse': (Adresse, 'comptes/supprimer_adresse.html')
    }

    # Vérifier si le type d'objet est valide
    if objet_type not in objets_mapping:
        raise Http404("Type d'objet invalide.")

    # Récupérer le modèle et le template correspondants
    objet_classe, template = objets_mapping[objet_type]

    # Récupérer l'objet avec son ID, en vérifiant que l'utilisateur a accès à l'objet
    if objet_type == 'entite':
        objet = get_object_or_404(objet_classe, id=objet_id)
    else:
        objet = get_object_or_404(objet_classe, id=objet_id, utilisateur=request.user)

    if request.method == 'POST':
        # Suppression de l'objet après confirmation
        objet.delete()
        messages.success(request, f'{objet_type.capitalize()} supprimé(e) avec succès !')
        return redirect('details', type='utilisateur', id=request.user.id)

    # Si GET, afficher la page de confirmation de suppression
    return render(request, template, {objet_type: objet})



@login_required
def liste_entites(request):
    # Récupérer toutes les entités
    entites = Entite.objects.all()
    profil = request.user.profil
    # Vérifier combien d'entités l'utilisateur a déjà choisies
    limite_atteinte = profil.entites.count() >= 3
    return render(request, 'comptes/entites.html', {
        'entites': entites,
        'limite_atteinte': limite_atteinte
    })



@login_required
def choisir_entite(request, entite_id):
    entite = get_object_or_404(Entite, id=entite_id)
    profil = request.user.profil

    # Vérifie si l'entité est déjà choisie
    if entite in profil.entites.all():
        messages.info(request, "Cette entité est déjà sélectionnée.")
        return redirect('details', type='entite', id=entite_id)

    # Vérifie combien d'entités l'utilisateur a déjà choisies
    if profil.entites.count() >= 3:
        # Message d'erreur ou redirection si plus de 3 entités sont déjà choisies
        messages.error(
            request, "Vous ne pouvez choisir que 3 entités maximum.")
        return redirect('liste_entites')  # Redirige vers la liste des entités

    # Ajoute l'entité choisie
    profil.entites.add(entite)
    messages.success(request, "Entité ajoutée avec succès.")
    return redirect('details', type='entite', id=entite_id)

@login_required
def deselectionner_entite(request, entite_id):
    entite = get_object_or_404(Entite, id=entite_id)
    profil = request.user.profil

    # Vérifie si l'entité est associée au profil de l'utilisateur
    if entite in profil.entites.all():
        profil.entites.remove(entite)
        messages.success(request, 'Entité désélectionnée avec succès !')
    else:
        messages.warning(request, 'Cette entité n\'est pas sélectionnée.')

    return redirect('liste_entites')


@login_required
def mise_a_jour_utilisateur(request):
    # Récupère l'utilisateur connecté
    utilisateur = request.user

    if request.method == 'POST':
        formulaire = FormulaireMiseAJourUtilisateur(
            request.POST, instance=utilisateur)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(
                request, 'Informations de l\'utilisateur modifiées avec succès !')
            # Redirige avec le type et l'ID de l'utilisateur
            return redirect('details', type='utilisateur', id=utilisateur.id)
    else:
        formulaire = FormulaireMiseAJourUtilisateur(instance=utilisateur)

    return render(request, 'comptes/mise_a_jour_utilisateur.html', {'formulaire': formulaire})


@login_required
def details(request, type, id):
    if type == 'utilisateur':
        # Récupère les études, adresses et entités de l'utilisateur
        etudes = Etude.objects.filter(utilisateur=request.user)
        adresses = Adresse.objects.filter(utilisateur=request.user)
        entites = request.user.profil.entites.all()

        return render(request, 'comptes/details_compte.html', {
            'utilisateur': request.user,
            'etudes': etudes,
            'adresses': adresses,
            'entites': entites,
        })
    
    elif type == 'entite':
        # Récupère l'entité par ID
        entite = get_object_or_404(Entite, id=id)
        return render(request, 'comptes/details_entite.html', {'entite': entite})
    
    else:
        # Gérer le cas où le type n'est pas reconnu
        return HttpResponseNotFound("Type non reconnu.")


@login_required
def confirmer_action(request, action_type):
    # Vérifier si l'action est valide (supprimer ou déconnecter)
    if action_type not in ['suppression', 'deconnexion']:
        raise Http404("Action non valide.")

    if request.method == 'POST':
        if action_type == 'suppression':
            utilisateur = request.user
            utilisateur.delete()  # Supprimer l'utilisateur
            messages.success(
                request, 'Votre compte a été supprimé avec succès.')
            # Rediriger vers la page d'accueil après suppression
            return redirect('accueil')
        elif action_type == 'deconnexion':
            logout(request)  # Déconnecter l'utilisateur
            messages.success(request, 'Vous êtes déconnecté avec succès.')
            # Rediriger vers la page d'accueil après déconnexion
            return redirect('accueil')

    # Définir le template en fonction de l'action
    template = 'comptes/confirmer_suppression_compte.html' if action_type == 'suppression' else 'comptes/confirmer_deconnexion.html'

    return render(request, template)

def charger_communes(request):
    id_departement = request.GET.get('departement')
    communes = Commune.objects.filter(departement_id=id_departement).values(
        'id', 'nom')  # Assurez-vous que 'name' est le bon champ
    return JsonResponse(list(communes), safe=False)







class Command(BaseCommand):
    help = 'Importer des départements et des communes à partir d\'un fichier CSV'

    def add_arguments(self, parser):
        parser.add_argument('fichier_csv', type=str)

    def handle(self, *args, **kwargs):
        fichier_csv = kwargs['fichier_csv']

        with open(fichier_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                nom_departement = row['departement'].strip()
                nom_commune = row['commune'].strip()

                # Vérifiez si le département existe, sinon créez-le
                departement, created = Departement.objects.get_or_create(
                    name=nom_departement)

                # Créez la commune associée au département
                Commune.objects.get_or_create(
                    name=nom_commune, departement=departement)

        self.stdout.write(self.style.SUCCESS(
            'Importation terminée avec succès.'))

@login_required
def demande_resultat_form(request):
    return render(request, 'demande_resultat_bacc.html')



@csrf_exempt  # N'utilise pas csrf_exempt en production sans réflexion
@login_required
def demande_resultat_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            matricule = data.get('matricule')
            date_naissance_str = data.get('date_naissance')
            programme = data.get('programme')
            
            # Convertir la date au format approprié
            date_naissance = datetime.strptime(date_naissance_str, '%d/%m/%Y').date()

            # Rechercher le bachelier dans la base de données
            bachelier = Bachelier.objects.filter(
                matricule=matricule,
                date_naissance=date_naissance,
                programme=programme
            ).first()

            if bachelier:
                resultat = {
                    'matricule': bachelier.matricule,
                    'nom': bachelier.nom,
                    'moyenne': bachelier.moyenne,
                    'mention': bachelier.mention,
                    'programme': bachelier.programme
                }
                return JsonResponse(resultat)
            else:
                return JsonResponse({'error': 'Aucun bachelier trouvé avec ces informations'}, status=404)

        except ValueError:
            return JsonResponse({'error': 'Données invalides'}, status=400)
    
    return JsonResponse({'error': 'Requête invalide'}, status=400)

def verification_diplome_view(request):
    return render(request, 'verification_diplome.html')

@csrf_exempt
def upload_scan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image')

            # Convertir l'image base64 en fichier image
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1]  
            file_path = f"media/scan.{ext}"  # Mettez à jour le chemin pour l'enregistrement dans un dossier 'media'
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(imgstr))
            
            return JsonResponse({'message': 'Scan reçu avec succès'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Requête non autorisée'}, status=400)

def e_document(request):
    # Générer une liste d'années de 1980 à l'année actuelle
    current_year = datetime.now().year
    years = list(range(1980, current_year + 1))  # Inclut l'année actuelle

    if request.method == "POST":
        # Récupérer les données du formulaire
        annee = request.POST.get('annee')
        matricule = request.POST.get('matricule')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')

        # Vérifier si les champs obligatoires sont remplis
        if not all([annee, matricule, nom, prenom, telephone]):
            error_message = "Tous les champs sont obligatoires."
            return render(request, 'e_document.html', {'years': years, 'error_message': error_message})

        # Traitement des données du formulaire (ajoutez votre logique ici)
        # Exemple: Sauvegarde dans une base de données ou envoi par email

        # Rediriger vers une page de succès
        return redirect('success_page')  # Vous pouvez créer une page 'success_page'

    return render(request, 'e_document.html', {'years': years})


