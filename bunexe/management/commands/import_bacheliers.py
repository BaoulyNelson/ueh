import csv
from django.core.management.base import BaseCommand
from bunexe.models import Bachelier

class Command(BaseCommand):
    help = "Importer des bacheliers depuis un fichier CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Chemin du fichier CSV à importer")

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                bachelier, created = Bachelier.objects.get_or_create(
                    matricule=row["matricule"],
                    defaults={
                        "nom": row["nom"],
                        "prenom": row["prenom"],
                        "date_naissance": row["date_naissance"],
                        "programme": row["programme"],
                        "creole": row["creole"],
                        "mathematiques": row["mathematiques"],
                        "physique": row["physique"],
                        "svt": row["svt"],
                        "chimie": row["chimie"],
                        "philosophie": row["philosophie"],
                        "anglais_espagnol": row["anglais_espagnol"],
                        "histoire_geo": row["histoire_geo"],
                        "economie": row["economie"],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Bachelier {bachelier.matricule} ajouté."))
                else:
                    self.stdout.write(self.style.WARNING(f"Bachelier {bachelier.matricule} existe déjà."))
