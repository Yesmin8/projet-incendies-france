import os
import pandas as pd
from geopy.distance import geodesic

INCENDIES_PATH = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_PACA.csv"
DOSSIER_METEO = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\PACA"
COLS_INCENDIES = ["Département", "Nom de la commune", "latitude", "longitude", "Date de première alerte"]
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
    
    return pd.Series([station_proche, round(min_distance, 3)], index=["station", "distance_km"])

def associer_stations():
    print("Chargement des incendies...")
    df_incendies = pd.read_csv(INCENDIES_PATH, sep=";", encoding="utf-8-sig", usecols=COLS_INCENDIES)
    df_incendies.dropna(subset=["latitude", "longitude", "Département"], inplace=True)
    df_incendies["Département"] = df_incendies["Département"].astype(str).str.zfill(2)

    print("Extraction des stations météo...")
    df_stations = extraire_stations_meteo(DOSSIER_METEO)
    df_stations.dropna(subset=["LAT", "LON", "DEPT", "NOM_USUEL"], inplace=True)
    df_stations["DEPT"] = df_stations["DEPT"].astype(str).str.zfill(2)

    print("Début de l'association aux stations météo...")
    stations_associees = []
    total = len(df_incendies)

    for i, row in df_incendies.iterrows():
        dept = row["Département"]
        stations_dept = df_stations[df_stations["DEPT"] == dept]
        resultat = trouver_station_proche(row, stations_dept)
        stations_associees.append(resultat)
        if (i + 1) % AFFICHAGE_PROGRESS == 0 or i == total - 1:
            print(f"{i + 1}/{total} lignes traitées...")

    df_resultats = pd.concat([df_incendies.reset_index(drop=True), pd.DataFrame(stations_associees)], axis=1)
    output_path = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\PACA\incendies_PACA_avec_station.csv"
    df_resultats.to_csv(output_path, sep=";", encoding="utf-8-sig", index=False)
    print(f"Fichier généré : {output_path} ({len(df_resultats)} lignes)")

if __name__ == "__main__":
    associer_stations()
