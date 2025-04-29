from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # << Import léger et propre

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('mon-profil/', views.mon_profil_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('moderateur/', views.moderateur_dashboard_view, name='moderateur_dashboard'),
    path('utilisateurs/', views.utilisateur_liste, name='utilisateur_liste'),
    path('commentaires/moderer/', views.commentaires_moderation, name='commentaires_moderation'),
    path('moderateur/parametres/', views.moderateur_parametres, name='moderateur_parametres'),
    path('commentaires/<int:commentaire_id>/approuver/', views.approuver_commentaire, name='approuver_commentaire'),
    path('commentaires/<int:commentaire_id>/supprimer/', views.supprimer_commentaire, name='supprimer_commentaire'),

    path('confirmer-deconnexion/', views.confirmer_deconnexion, name='confirmer_deconnexion'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='comptes/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='comptes/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='comptes/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='comptes/password_reset_complete.html'), name='password_reset_complete'),

    

    path('resultatbac/', views.demande_resultat_form, name='demande_resultat_bac'),
    path('api/demande-resultat/', views.demande_resultat_ajax, name='demande_resultat_ajax'),
    path('api/generate-csv/<str:matricule>/<str:date_naissance>/<str:programme>/', views.generate_csv, name='generate_csv'),
    
    path('verification-diplome/', views.verification_diplome_view, name='verification_diplome'),
    path('e-document/', views.e_document, name='e_document'),
    path('success/', views.success_page, name='success_page'),
    path('examens/', views.examens_view, name='examens'),
    path('contact/', views.contact_view, name='contact'),
]
