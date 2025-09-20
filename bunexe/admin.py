from django.contrib import admin
from .models import Commentaire
from .models import Bachelier,Examen,Article,Commentaire
# Register your models here.

# Crée une classe d'administration pour personnaliser l'affichage des articles
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'image')  # Liste les champs à afficher dans la liste des articles
    search_fields = ('title', 'content')  # Permet de chercher par titre et contenu
    list_filter = ('date',)  # Permet de filtrer les articles par date
    ordering = ('-date',)  # Trie les articles par date décroissante par défaut



@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date', 'status')
    search_fields = ('titre', 'description')
    list_filter = ('status',)

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'date_poste', 'approbation')
    list_filter = ('approbation',)
    search_fields = ('texte', 'auteur__username')

# admin.py
from django.contrib import admin
from .models import Bachelier

from django.contrib import admin
from .models import Bachelier

@admin.register(Bachelier)
class BachelierAdmin(admin.ModelAdmin):
    list_display = ("matricule", "nom", "prenom", "programme", "get_moyenne", "get_mention")
    search_fields = ("matricule", "nom", "prenom")
    list_filter = ("programme",)
    ordering = ("nom",)
    fields = (
        "matricule",
        "nom",
        "prenom",
        "date_naissance",
        "programme",
        "creole",
        "mathematiques",
        "physique",
        "svt",
        "chimie",
        "philosophie",
        "anglais_espagnol",
        "histoire_geo",
        "economie",
    )
    readonly_fields = ("get_moyenne", "get_mention")

admin.site.register(Article, ArticleAdmin)
