import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from ueh.models import Entite  # Assure-toi que le chemin du modèle est correct


class Command(BaseCommand):
    help = 'Importe les entités depuis un fichier CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', type=str, help='Le chemin vers le fichier CSV contenant les entités')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                created_entities = 0

                for row in reader:
                    # Nettoyage des espaces
                    entity_name = row.get('name', '').strip()
                    
                    # Debugging : Affiche ce qui est lu pour chaque ligne
                    self.stdout.write(f"Entity Name from CSV: {entity_name}")

                    # Validation simple
                    if not entity_name:
                        self.stdout.write(self.style.ERROR(
                            f"Ligne ignorée (nom d'entité manquant) : {row}"))
                        continue

                    # Créer ou récupérer l'entité
                    try:
                        entite, created = Entite.objects.get_or_create(
                            nom=entity_name)
                        if created:
                            created_entities += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f"Erreur lors de la création de l'entité : {entity_name} - {str(e)}"))

                # Résumé de l'importation
                self.stdout.write(self.style.SUCCESS(
                    f"Importation terminée : {created_entities} entités créées."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Fichier {csv_file} non trouvé"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Erreur lors de l'importation : {str(e)}"))
