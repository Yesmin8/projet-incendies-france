import os
import shutil
import re

# Obtenir le dossier où se trouve ce script (et donc les fichiers .nc)
dossier_base = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\era5\NA"

# Parcours de tous les fichiers dans le dossier
for nom_fichier in os.listdir(dossier_base):
    if nom_fichier.endswith(".nc"):
        # Extraire la date (format AAAA-MM-JJ)
        match = re.search(r"\d{4}-\d{2}-\d{2}", nom_fichier)
        if match:
            annee = match.group()[:4]

            # Créer un dossier pour l'année s’il n’existe pas encore
            dossier_annee = os.path.join(dossier_base, annee)
            os.makedirs(dossier_annee, exist_ok=True)

            # Déplacer le fichier dans le bon dossier
            chemin_source = os.path.join(dossier_base, nom_fichier)
            chemin_destination = os.path.join(dossier_annee, nom_fichier)

            # Vérification si le fichier existe déjà dans le dossier de destination
            if not os.path.exists(chemin_destination):
                shutil.move(chemin_source, chemin_destination)
                print(f"Déplacé : {nom_fichier} → {annee}/")
            else:
                print(f"Fichier déjà présent : {nom_fichier} (non déplacé)")
        else:
            print(f"Aucune date trouvée dans le nom : {nom_fichier}")
