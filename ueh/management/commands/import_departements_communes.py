import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from ueh.models import Departement, Commune

class Command(BaseCommand):
    help = 'Import departments and communes from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                created_departments = 0
                created_communes = 0

                for row in reader:
                    department_name = row.get('Departement')
                    commune_name = row.get('Commune')

                    # Validation simple
                    if not department_name or not commune_name:
                        self.stdout.write(self.style.ERROR(f"Ligne ignorée : {row}"))
                        continue

                    # Créer ou récupérer le département
                    departement, created = Departement.objects.get_or_create(nom=department_name)
                    if created:
                        created_departments += 1

                    # Créer ou récupérer la commune
                    commune, created = Commune.objects.get_or_create(nom=commune_name, departement=departement)
                    if created:
                        created_communes += 1

                # Résumé de l'importation
                self.stdout.write(self.style.SUCCESS(f"Importation terminée : {created_departments} départements créés, {created_communes} communes créées."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Fichier {csv_file} non trouvé"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation : {str(e)}"))
