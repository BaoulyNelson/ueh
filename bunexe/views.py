from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User  # ou ton modèle personnalisé
from django.views.decorators.http import require_POST
from bunexe.utils import ajouter_message
from django.urls import reverse

from datetime import datetime
import json
import base64
import csv

from .models import Bachelier, Article, Examen,Commentaire,Verification
from .forms import (
    FormulaireCreationUtilisateur,
    FormulaireAuthentificationPersonnalise,
    DocumentSearchForm,
    BaccalaureatForm,FormulaireMiseAJourUtilisateur,ContactForm
)



def accueil(request):
    articles = Article.objects.all().order_by('-date')
    commentaires = Commentaire.objects.filter(approbation=True).order_by('-date_poste')[:5]  # les 5 derniers commentaires approuvés

    ARTICLES_PER_PAGE = 5
    paginator = Paginator(articles, ARTICLES_PER_PAGE)
    page_number = request.GET.get('page')

    try:
        paginated_articles = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_articles = paginator.page(1)
    except EmptyPage:
        paginated_articles = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'main_articles': paginated_articles,
        'side_articles': articles[:5],
        'commentaires': commentaires,
    })



def connexion(request):
    next_url = request.GET.get("next", "accueil")  # Valeur par défaut = accueil

    if request.method == 'POST':
        formulaire = FormulaireAuthentificationPersonnalise(request, data=request.POST)

        if formulaire.is_valid():
            user = formulaire.get_user()
            login(request, user)

            # Se souvenir de moi (2 semaines = 14 jours)
            if 'remember_me' in request.POST:
                request.session.set_expiry(60 * 60 * 24 * 14)  # 14 jours
            else:
                request.session.set_expiry(0)  # Expire à la fermeture du navigateur

            messages.success(request, f"Bienvenue {user.username} ! 😊 Vous êtes connecté.")
            
            return redirect(request.POST.get("next", next_url))  # Redirection dynamique

        else:
            messages.error(request, 'Identifiants invalides. Veuillez réessayer.')
    else:
        formulaire = FormulaireAuthentificationPersonnalise()

    return render(request, 'comptes/connexion.html', {'formulaire': formulaire, 'next': next_url})



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
def mon_profil_view(request):
    return render(request, 'comptes/profile.html')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = FormulaireMiseAJourUtilisateur(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            ajouter_message(request, 'success', "Votre profil a été mis à jour avec succès.")
            return redirect('profile')
        else:
            ajouter_message(request, 'error', "Une erreur s'est produite lors de la mise à jour.")
    else:
        form = FormulaireMiseAJourUtilisateur(instance=request.user)
    
    return render(request, 'comptes/edit_profile.html', {'form': form})



@login_required
def moderateur_dashboard_view(request):
    return render(request, 'comptes/moderateur.html')


@login_required
def utilisateur_liste(request):
    users = User.objects.all()
    return render(request, 'comptes/utilisateur_liste.html', {'users': users})


@login_required
def commentaires_moderation(request):
    commentaires = Commentaire.objects.filter(approbation=False).order_by('-date_poste')
    return render(request, 'comptes/commentaires_moderation.html', {'commentaires': commentaires})




@require_POST
@login_required
def approuver_commentaire(request, commentaire_id):
    commentaire = get_object_or_404(Commentaire, id=commentaire_id)
    commentaire.approbation = True
    commentaire.save()
    return redirect('commentaires_moderation')



@require_POST
@login_required
def supprimer_commentaire(request, commentaire_id):
    commentaire = get_object_or_404(Commentaire, id=commentaire_id)
    commentaire.delete()
    return redirect('commentaires_moderation')



@login_required
def moderateur_parametres(request):
    return render(request, 'comptes/moderateur_parametres.html')


@login_required
def confirmer_deconnexion(request):
    if request.method == 'POST':
        logout(request)
        ajouter_message(request, 'success', "Vous vous êtes déconnecté avec succès.")
        return redirect('accueil')
    return render(request, 'comptes/confirmer_deconnexion.html')


def article_detail(request, article_id):
    # Récupère l'article principal
    article = get_object_or_404(Article, id=article_id)

    # Exclut l'article actuel et trie par date
    side_articles_list = Article.objects.exclude(id=article.id).order_by('-date')

    # Pagination pour les articles secondaires
    ARTICLES_PER_PAGE = 5
    paginator = Paginator(side_articles_list, ARTICLES_PER_PAGE)
    page_number = request.GET.get('side_page')

    try:
        side_articles = paginator.page(page_number)
    except PageNotAnInteger:
        side_articles = paginator.page(1)  # Affiche la première page si ce n'est pas un entier
    except EmptyPage:
        side_articles = paginator.page(paginator.num_pages)  # Affiche la dernière page si le numéro est trop grand

    return render(request, 'articles/article_detail.html', {
        'article': article,
        'side_articles': side_articles  # Articles paginés
    })



def success_page(request):
    return render(request, 'success.html')  # Assure-toi d’avoir un fichier success.html


from django.shortcuts import render
from datetime import datetime
from .models import Bachelier
from .forms import DocumentSearchForm

def e_document(request):
    current_year = datetime.now().year
    years = list(range(1980, current_year + 1))  # années disponibles
    releve = None
    erreur = None

    if request.method == "POST":
        form = DocumentSearchForm(request.POST, years=years)
        if form.is_valid():
            annee = form.cleaned_data['annee']
            matricule = form.cleaned_data['matricule']
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']

            try:
                bachelier = Bachelier.objects.get(
                    matricule=matricule,
                    nom__iexact=nom,
                    prenom__iexact=prenom,
                    annee_bac=annee
                )
                releve = {
                    "nom": bachelier.nom.upper(),
                    "prenom": bachelier.prenom.title(),
                    "date_naissance": bachelier.date_naissance,
                    "annee": annee,
                    "total": bachelier.calcul_total(),
                    "max_total": 1900,  # ou 1900 selon ton calcul
                    "moyenne": bachelier.moyenne,
                    "mention": bachelier.mention,
                    "programme": bachelier.programme,
                }
            except Bachelier.DoesNotExist:
                erreur = "Aucun résultat trouvé pour ces informations."
    else:
        form = DocumentSearchForm(years=years)

    return render(request, 'resultats/e_document.html', {
        'form': form,
        'releve': releve,
        'erreur': erreur
    })





def demande_resultat_form(request):
    bachelier = None
    erreur = None

    # Toujours récupérer ou créer l'objet Statistique
    stats, created = Verification.objects.get_or_create(id=1)

    if request.method == "POST":
        matricule = request.POST.get("matricule", "").strip()

        # Vérification du matricule
        if len(matricule) != 10 or not matricule.isdigit():
            request.session["erreur"] = "Il faut saisir un matricule ayant 10 chiffres"
        else:
            # Incrémenter le compteur global
            stats.verifications += 1
            stats.save()

            try:
                bachelier = Bachelier.objects.get(matricule=matricule)
                request.session["last_bachelier"] = bachelier.id
            except Bachelier.DoesNotExist:
                request.session["erreur"] = "Pas de données pour l'instant"

        return redirect(reverse("demande_resultat_bac"))

    # Après redirection, récupérer la session
    if "last_bachelier" in request.session:
        try:
            bachelier = Bachelier.objects.get(id=request.session.pop("last_bachelier"))
        except Bachelier.DoesNotExist:
            pass

    if "erreur" in request.session:
        erreur = request.session.pop("erreur")

    # Préparer les matières avec le seuil de moitié du coefficient
    matieres = []
    if bachelier:
        for champ, coef, nom in [
            ("creole", 200, "Créole"),
            ("mathematiques", 200, "Mathématiques"),
            ("physique", 100, "Physique"),
            ("svt", 100, "SVT"),
            ("chimie", 100, "Chimie"),
            ("philosophie", 200, "Philosophie"),
            ("anglais_espagnol", 200, "Anglais / Espagnol"),
            ("histoire_geo", 400, "Histoire & Géographie"),
            ("economie", 400, "Économie"),
        ]:
            note = getattr(bachelier, champ)
            seuil = coef / 2
            matieres.append((nom, note, coef, seuil))

    # Récupérer à nouveau le compteur à jour pour l'affichage
    stats.refresh_from_db()

    return render(request, "resultats/demande_resultat_bacc.html", {
        "form": BaccalaureatForm(),
        "bachelier": bachelier,
        "matieres": matieres,
        "erreur": erreur,
        "verifications": stats.verifications,
    })




@csrf_exempt  # ⚠️ Éviter en production, utiliser `@csrf_protect` ou `@ensure_csrf_cookie`
@login_required
def demande_resultat_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = BaccalaureatForm(data)

            if form.is_valid():
                matricule = form.cleaned_data['matricule']
                date_naissance_str = form.cleaned_data['date_naissance']
                programme = form.cleaned_data['programme']

                # ✅ Vérifier si c'est déjà une date, sinon convertir
                if isinstance(date_naissance_str, str):
                    date_naissance = datetime.strptime(date_naissance_str, "%Y-%m-%d").date()
                else:
                    date_naissance = date_naissance_str  # Elle est déjà sous format date

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
            
            return JsonResponse({'error': 'Données invalides', 'details': form.errors}, status=400)

        except ValueError:
            return JsonResponse({'error': 'Format des données incorrect'}, status=400)
    
    return JsonResponse({'error': 'Requête invalide'}, status=400)


def generate_csv(request, matricule, date_naissance, programme):
    # Recherche des résultats
    bachelier = Bachelier.objects.filter(
        matricule=matricule,
        date_naissance=date_naissance,
        programme=programme
    ).first()

    if not bachelier:
        return JsonResponse({'error': 'Aucun bachelier trouvé'}, status=404)

    # Ici, tu dois adapter cette partie pour générer le CSV correctement
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="resultat_{matricule}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Matricule', 'Nom', 'Moyenne', 'Mention'])  # Entêtes du fichier CSV

 # Par exemple, récupérer le bachelier à partir des paramètres
    bachelier = Bachelier.objects.filter(
        matricule=matricule,
        date_naissance=date_naissance,
        programme=programme
    ).first()

    if bachelier:
        writer.writerow([bachelier.matricule, bachelier.nom, bachelier.moyenne, bachelier.mention])
    else:
        writer.writerow(['Aucun résultat trouvé'])

    return response



def verification_diplome_view(request):
    return render(request, 'resultats/verification_diplome.html')

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


def examens_view(request):
    examens = Examen.objects.all()
    return render(request, 'examens/examen.html', {'examens': examens})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # <-- ENREGISTRE EN BASE
            return render(request, "contact/contact_success.html")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})