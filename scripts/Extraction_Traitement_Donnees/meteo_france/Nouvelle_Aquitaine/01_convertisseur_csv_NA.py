import os
import gzip
import shutil

DOSSIER_BASE_INPUT = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\meteo_france\NA"
DOSSIER_BASE_OUTPUT = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\Nouvelle_Aquitaine"


print(f"Dossier racine : {DOSSIER_BASE_INPUT}\n")

# Parcours de tous les sous-dossiers
for Departement in os.listdir(DOSSIER_BASE_INPUT):
    chemin_dep = os.path.join(DOSSIER_BASE_INPUT, Departement)
    if os.path.isdir(chemin_dep):
        print(f"Département : {Departement}")
        
        for file in os.listdir(chemin_dep):
            if file.endswith(".csv.gz"):
                chemin_gz = os.path.join(chemin_dep, file)
                
                # Créer le dossier de sortie pour le département si il n'existe pas
                dossier_output_dep = os.path.join(DOSSIER_BASE_OUTPUT, Departement)
                os.makedirs(dossier_output_dep, exist_ok=True)

                chemin_csv = os.path.join(dossier_output_dep, file.replace(".csv.gz", ".csv"))

                if not os.path.exists(chemin_csv):
                    print(f"Décompression : {file}")
                    try:
                        with gzip.open(chemin_gz, 'rb') as f_in:
                            with open(chemin_csv, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        print(f"Fichier créé : {chemin_csv}")
                    except Exception as e:
                        print(f"Erreur avec {file} : {e}")
                else:
                    print(f"Déjà existant : {file.replace('.csv.gz', '.csv')}")
        print()

