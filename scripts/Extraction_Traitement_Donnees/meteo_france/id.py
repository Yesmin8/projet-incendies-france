import pandas as pd

def associer_id_incendie(chemin_meteo, chemin_incendies, chemin_sortie):
    print(f"\n Traitement en cours :\n  Incendies = {chemin_incendies}\n  Météo     = {chemin_meteo}")

    # === Chargement des fichiers ===
    print("Chargement des fichiers...")
    df_incendies = pd.read_csv(chemin_incendies, sep=";", encoding="utf-8-sig")
    df_meteo = pd.read_csv(chemin_meteo, sep=";", encoding="utf-8-sig")

    # === Conversion des dates ===
    print("Conversion des dates...")
    df_incendies['Date de première alerte'] = pd.to_datetime(df_incendies['Date de première alerte'], errors='coerce')
    df_meteo['date_heure'] = pd.to_datetime(df_meteo['date_heure'], errors='coerce')

    # === Normalisation des noms de stations ===
    print("Nettoyage des noms de stations...")
    df_incendies['station_norm'] = df_incendies['station'].str.strip().str.lower()
    df_meteo['station_norm'] = df_meteo['nom_station'].str.strip().str.lower()

    # === Fonction d'association ===
    def associer_incendie(row):
        station = row['station_norm']
        date_meteo = row['date_heure']

        candidats = df_incendies[df_incendies['station_norm'] == station]
        if candidats.empty:
            return None

        candidats = candidats.copy()
        candidats['ecart'] = abs((candidats['Date de première alerte'] - date_meteo).dt.total_seconds())
        incendie_proche = candidats.sort_values('ecart').iloc[0]
        return incendie_proche['id']

    print("Association des lignes météo aux incendies...")
    df_meteo['id_incendie'] = df_meteo.apply(associer_incendie, axis=1)

    # === Réorganisation des colonnes ===
    print("Réorganisation des colonnes...")
    colonnes = ['id_incendie'] + [col for col in df_meteo.columns if col != 'id_incendie']
    df_meteo = df_meteo[colonnes]

    # === Sauvegarde ===
    print(f"Sauvegarde du fichier vers : {chemin_sortie}")
    df_meteo.to_csv(chemin_sortie, sep=";", encoding="utf-8-sig", index=False)

    print(f"Terminé : {chemin_sortie}")


# === TRAITEMENT NOUVELLE-AQUITAINE ===
associer_id_incendie(
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\Nouvelle_Aquitaine\donnees_meteo_france_NA.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\incendies\Incendies_Nouvelle_Aquitaine.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\meteo_france\donnees_meteo_france_NA.csv"
)

# === TRAITEMENT PACA ===
associer_id_incendie(
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\PACA\donnees_meteo_france_PACA.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\incendies\Incendies_PACA.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\meteo_france\donnees_meteo_france_PACA.csv"
)
