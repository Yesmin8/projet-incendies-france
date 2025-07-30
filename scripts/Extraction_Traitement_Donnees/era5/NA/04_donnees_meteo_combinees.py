import os
import pandas as pd

# === PARAMÈTRES ===
DOSSIER_BASE_CSV = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\ERA5\Nouvelle_Aquitaine"
CHEMIN_CSV_COMBINE = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\ERA5\donnees_meteo_combinees_NA.csv"

def concatener_et_trier_par_blocs(dossier_base_csv, chemin_csv_combine, separateur):
    blocs = []
    erreurs = []
    total_fichiers = 0

    print(f"\n--- CONCATÉNATION PAR FICHIER (BLOC INCENDIE) ---\n")

    for racine, _, fichiers in os.walk(dossier_base_csv):
        for fichier in fichiers:
            if fichier.endswith(".csv") and fichier.startswith("meteo_"):
                chemin_csv = os.path.join(racine, fichier)
                try:
                    df = pd.read_csv(chemin_csv, sep=separateur, encoding="utf-8-sig")
                    if 'datetime' not in df.columns:
                        raise ValueError("Colonne 'datetime' manquante")
                    
                    # Convertir en datetime
                    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

                    # Ajouter colonne "date_bloc" = première datetime du fichier
                    df['date_bloc'] = df['datetime'].min()

                    # Pour retrouver les blocs facilement : nom du fichier
                    df['fichier_source'] = fichier

                    blocs.append(df)
                    total_fichiers += 1

                except Exception as e:
                    erreurs.append(f"{chemin_csv} : {e}")
                    print(f"Erreur : {chemin_csv} : {e}")

    if not blocs:
        print("Aucun fichier trouvé.")
        return

    # Concaténer tous les blocs
    df_combine = pd.concat(blocs, ignore_index=True)

    # Trier par date du bloc (pas ligne par ligne)
    df_combine = df_combine.sort_values(by=["date_bloc", "fichier_source", "datetime"])

    # Supprimer colonnes temporaires
    df_combine = df_combine.drop(columns=["date_bloc", "fichier_source"])

    # Sauvegarde
    try:
        df_combine.to_csv(chemin_csv_combine, index=False, sep=separateur, encoding="utf-8-sig")
        print(f"\n Fichier final créé : {chemin_csv_combine}")
        print(f" Fichiers traités : {total_fichiers}")
    except Exception as e:
        print(f"\n Erreur d'enregistrement : {e}")

    # Affichage des erreurs
    if erreurs:
        print(f"\n {len(erreurs)} erreurs rencontrées :")
        for err in erreurs:
            print(f"- {err}")

# === EXÉCUTION ===
concatener_et_trier_par_blocs(DOSSIER_BASE_CSV, CHEMIN_CSV_COMBINE, ';')
