from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class Departement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Commune(models.Model):
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, related_name='communes', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class Adresse(models.Model):
    no = models.CharField(max_length=10)  # Numéro de rue ou de maison
    adresse = models.CharField(max_length=255)  # Adresse complète (rue)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)  # Département associé
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)  # Commune associée
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisateur associé

    def __str__(self):
        return f"{self.no}, {self.adresse}, {self.commune.nom}, {self.departement.nom}"


class Diplome(models.Model):
    DIPLOME_CHOIX = [
        ('Licence', 'Licence'),
        ('Master', 'Master'),
        ('Doctorat', 'Doctorat'),
    ]
    
    type_diplome = models.CharField(max_length=50, choices=DIPLOME_CHOIX)
    
    def __str__(self):
        return self.type_diplome



class Etude(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    NIVEAU_CHOIX = [
        ('Bacc2', 'Bacc2'),
        ('Bac unique', 'Bac unique'),
        ('Post-secondaire', 'Post-secondaire'),
        ('NS4', 'NS4'),
    ]
    niveau = models.CharField(max_length=50, choices=NIVEAU_CHOIX)
    institution = models.CharField(max_length=255)
    annee = models.PositiveIntegerField()  # Assure-toi de valider l'année
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.niveau} - {self.institution} ({self.annee})"


class Entite(models.Model):
    nom = models.CharField(max_length=255, unique=True)
   

    def __str__(self):
        return self.nom

    

class Profil(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.ForeignKey(Adresse, on_delete=models.SET_NULL, null=True, blank=True)
    etudes = models.ManyToManyField(Etude, blank=True)
    entites = models.ManyToManyField(Entite, blank=True)

    def __str__(self):
        return self.utilisateur.username



class Bachelier(models.Model):
    matricule = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    programme = models.CharField(max_length=100)
    moyenne = models.CharField(max_length=10)
    mention = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} ({self.matricule})"