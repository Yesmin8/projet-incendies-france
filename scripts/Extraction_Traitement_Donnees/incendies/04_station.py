import os
import pandas as pd
from geopy.distance import geodesic

# === Paramètres globaux ===
REGIONS = {
    "Nouvelle_Aquitaine": {
        "incendies_path": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_Nouvelle_Aquitaine.csv",
        "meteo_dir": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\Nouvelle_Aquitaine",
        "output_path": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_Nouvelle_Aquitaine.csv"
    },
    "PACA": {
        "incendies_path": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_PACA.csv",
        "meteo_dir": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\PACA",
        "output_path": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_PACA.csv"
    }
}

AFFICHAGE_PROGRESS = 100

def extraire_stations_meteo(dossier_base):
    stations = []
    for nom_dossier in os.listdir(dossier_base):
        chemin_dossier = os.path.join(dossier_base, nom_dossier)
        if os.path.isdir(chemin_dossier) and nom_dossier.startswith("Departement_"):
            dept_num = nom_dossier.split("_")[1]
            for fichier in os.listdir(chemin_dossier):
                if fichier.startswith("H_") and fichier.endswith(".csv"):
                    chemin_fichier = os.path.join(chemin_dossier, fichier)
                    try:
                        df = pd.read_csv(chemin_fichier, sep=";", encoding="utf-8-sig", usecols=["NOM_USUEL", "LAT", "LON"])
                        df.drop_duplicates(inplace=True)
                        df["DEPT"] = dept_num
                        stations.append(df)
                    except Exception as e:
                        print(f"Erreur lecture {chemin_fichier} : {e}")
    if not stations:
        raise ValueError("Aucune station météo trouvée.")
    return pd.concat(stations, ignore_index=True).drop_duplicates()

def trouver_station_proche(row, stations_dept):
    point_incendie = (row["latitude"], row["longitude"])
    min_distance = float("inf")
    station_proche = None

    for _, station in stations_dept.iterrows():
        point_station = (station["LAT"], station["LON"])
        distance = geodesic(point_incendie, point_station).kilometers
        if distance < min_distance:
            min_distance = distance
            station_proche = station["NOM_USUEL"]
    
    return station_proche

def traiter_region(nom_region, chemin_incendies, dossier_meteo, chemin_output):
    print(f"\n=== Traitement région : {nom_region} ===")
    print("Chargement des données d'incendies...")
    df_incendies = pd.read_csv(chemin_incendies, sep=";", encoding="utf-8-sig")
    df_incendies.dropna(subset=["latitude", "longitude", "Département"], inplace=True)
    df_incendies["Département"] = df_incendies["Département"].astype(str).str.zfill(2)

    print("Chargement des stations météo...")
    df_stations = extraire_stations_meteo(dossier_meteo)
    df_stations.dropna(subset=["LAT", "LON", "DEPT", "NOM_USUEL"], inplace=True)
    df_stations["DEPT"] = df_stations["DEPT"].astype(str).str.zfill(2)

    print("Association des incendies aux stations les plus proches...")
    stations_proches = []
    total = len(df_incendies)

    for i, row in df_incendies.iterrows():
        dept = row["Département"]
        stations_dept = df_stations[df_stations["DEPT"] == dept]
        station = trouver_station_proche(row, stations_dept)
        stations_proches.append(station)
        if (i + 1) % AFFICHAGE_PROGRESS == 0 or i == total - 1:
            print(f"{i + 1}/{total} lignes traitées...")

    # Insertion en colonne D (index 3)
    df_incendies.insert(3, "station", stations_proches)

    # Sauvegarde
    os.makedirs(os.path.dirname(chemin_output), exist_ok=True)
    df_incendies.to_csv(chemin_output, sep=";", encoding="utf-8-sig", index=False)
    print(f"Fichier enregistré : {chemin_output} ({len(df_incendies)} lignes)")

if __name__ == "__main__":
    for region, params in REGIONS.items():
        traiter_region(
            nom_region=region,
            chemin_incendies=params["incendies_path"],
            dossier_meteo=params["meteo_dir"],
            chemin_output=params["output_path"]
        )
