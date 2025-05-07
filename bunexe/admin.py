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

# Enregistre le modèle Article avec l'administration Django
admin.site.register(Bachelier)

admin.site.register(Article, ArticleAdmin)
