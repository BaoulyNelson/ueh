from django.urls import path
from .views import (
    accueil, inscription, connexion, confirmer_action, mise_a_jour_utilisateur,
    charger_communes, ajouter_objet,modifier_objet,supprimer_objet, liste_entites, choisir_entite, deselectionner_entite,details,demande_resultat_ajax,verification_diplome_view,e_document,demande_resultat_form
)


urlpatterns = [
    path('', accueil, name='accueil'),  # Page d'accueil
    
    path('inscription/', inscription, name='inscription'),  # Inscription
    
    path('communes/', charger_communes, name='charger_communes'),  # Charger les communes
    
    path('connexion/', connexion, name='connexion'),  # Connexion
    
   
    path('details/<str:type>/<int:id>/', details, name='details'),
    
    
    # Mise à jour avec un paramètre pour le type d'objet
    path('utilisateur/modifier/', mise_a_jour_utilisateur, name='modifier_utilisateur'),

    path('confirmer/<str:action_type>/', confirmer_action, name='confirmer_action'),
    
    path('ajouter/<str:objet_type>/', ajouter_objet, name='ajouter_objet'),
    
    path('modifier/<str:objet_type>/<int:objet_id>/', modifier_objet, name='modifier_objet'),
    path('supprimer/<str:objet_type>/<int:objet_id>/', supprimer_objet, name='supprimer_objet'),


    path('ajax/charger-communes/', charger_communes, name='ajax_charger_communes'),  # Charger communes via AJAX
    
    path('entites/', liste_entites, name='liste_entites'),
    
    path('entites/<int:entite_id>/choisir/', choisir_entite, name='choisir_entite'),
    
    
    path('entites/<int:entite_id>/deselectionner/', deselectionner_entite, name='deselectionner_entite'),  # Ajoute cette ligne



    path('demande-resultat-bac/', demande_resultat_form, name='demande_resultat_bac'),  # Vue pour le formulaire
    path('api/demande-resultat/', demande_resultat_ajax, name='demande_resultat_ajax'),  # Vue pour l'AJAX


    path('verification-diplome/', verification_diplome_view, name='verification_diplome'),  # Nouvelle entrée
    path('e-document/', e_document, name='e_document'),  # URL pour la vue e_document

]
