from django.db import models
from django.contrib.auth.models import User

class Bachelier(models.Model):
    matricule = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    programme = models.CharField(max_length=100)
    moyenne = models.CharField(max_length=10)
    mention = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} ({self.matricule})"
    


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
