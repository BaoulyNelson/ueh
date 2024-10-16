from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profil  # Utilisation du modèle Profil

# Signal pour créer automatiquement un profil lors de la création d'un utilisateur
@receiver(post_save, sender=User)
def creer_profil_utilisateur(sender, instance, created, **kwargs):
    """Crée un profil utilisateur lorsque l'utilisateur est créé."""
    if created:
        Profil.objects.create(utilisateur=instance)  # Utiliser 'utilisateur' au lieu de 'user'


# Signal pour sauvegarder automatiquement les modifications du profil lors de la sauvegarde de l'utilisateur
@receiver(post_save, sender=User)
def sauvegarder_profil_utilisateur(sender, instance, **kwargs):
    """Sauvegarde le profil associé à l'utilisateur lorsque l'utilisateur est sauvegardé."""
    try:
        instance.profil.save()  # Utiliser 'profil' si la relation est modifiée dans User
    except Profil.DoesNotExist:
        # Gérer le cas où le profil n'existe pas (bien que cela ne devrait pas arriver)
        pass
