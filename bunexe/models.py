from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin

from django.db import models

class Bachelier(models.Model):
    matricule = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    date_naissance = models.DateField()
    programme = models.CharField(max_length=100)
    annee_bac = models.IntegerField(default=2025)  # <-- nouveau champ pour l'année du bac

    # Notes par matière
    creole = models.IntegerField()
    mathematiques = models.IntegerField()
    physique = models.IntegerField()
    svt = models.IntegerField()
    chimie = models.IntegerField()
    philosophie = models.IntegerField()
    anglais_espagnol = models.IntegerField()
    histoire_geo = models.IntegerField()
    economie = models.IntegerField()

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"

    # Calcul du total simple
    def calcul_total(self):
        return (
            self.creole + self.mathematiques + self.physique + self.svt +
            self.chimie + self.philosophie + self.anglais_espagnol +
            self.histoire_geo + self.economie
        )

    # Moyenne sur 10
    def get_moyenne(self):
        total = self.calcul_total()
        return round(total / 1900 * 10, 2)

    # Mention
    def get_mention(self):
        total = self.calcul_total()
        return "Admis" if total >= 950 else "Echoué(e)"

    # Pour accéder dans Django admin comme propriété
    @property
    def moyenne(self):
        return self.get_moyenne()

    @property
    def mention(self):
        return self.get_mention()




class Verification(models.Model):
    verifications = models.PositiveIntegerField(default=0)
    
    
class Examen(models.Model):
    date = models.DateField()  # Champ de type Date
    titre = models.CharField(max_length=255)
    description = models.TextField()
    
    STATUS_CHOICES = [
        ('completed', 'Terminé'),
        ('active', 'En cours'),
        ('upcoming', 'À venir'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.titre

   
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)  # Définit la date automatiquement à la création
    image = models.ImageField(upload_to='articles/images/')
    author = models.CharField(max_length=100, default='MENFP')  # Auteur par défaut

    def __str__(self):
        return self.title



class Contact(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    sujet = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    

class Commentaire(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date_poste = models.DateTimeField(auto_now_add=True)
    approbation = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.auteur.username} - {self.texte[:30]}..."
