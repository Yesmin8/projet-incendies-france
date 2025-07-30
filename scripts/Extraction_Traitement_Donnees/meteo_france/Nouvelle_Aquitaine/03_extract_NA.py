import os
import pandas as pd

# === PARAMÈTRES ===
FICHIER_INCENDIES = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\Nouvelle_Aquitaine\incendies_NA_avec_station.csv"
DOSSIER_METEO = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\Nouvelle_Aquitaine"
FICHIER_SORTIE = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\Nouvelle_Aquitaine\donnees_meteo_france_NA.csv"

def charger_groupes_regroupes():
    df = pd.read_csv(FICHIER_INCENDIES, sep=";", encoding="utf-8-sig", usecols=["Département", "station", "Date de première alerte"])
    df["Département"] = df["Département"].astype(str).str.zfill(2)
    df["Date_aaaammjj"] = pd.to_datetime(df["Date de première alerte"], dayfirst=True).dt.strftime("%Y%m%d")
    return df.groupby(["Département", "station"])["Date_aaaammjj"].unique().reset_index()

def charger_fichiers_meteo_du_departement(dept_num):
    dossier = os.path.join(DOSSIER_METEO, f"Departement_{dept_num}")
    return [os.path.join(dossier, f) for f in os.listdir(dossier) if f.startswith("H_") and f.endswith(".csv")]

def extraire_donnees_station_dates(fichiers, nom_station, dates):
    frames = []
    for fichier in fichiers:
        try:
            df = pd.read_csv(fichier, sep=";", encoding="utf-8-sig")
            df = df[df["NOM_USUEL"] == nom_station]
            df = df[df["AAAAMMJJHH"].astype(str).str[:8].isin(dates)]
            if not df.empty:
                frames.append(df)
        except Exception as e:
            print(f"Erreur fichier {fichier} : {e}")
    if frames:
        return pd.concat(frames, ignore_index=True)
    else:
        return pd.DataFrame()

def main():
    print("Regroupement des incendies par département/station...")
    groupes = charger_groupes_regroupes()
    all_data = []

    total = len(groupes)
    print(f"Total de groupes à traiter : {total}")
    
    for idx, row in groupes.iterrows():
        dept = row["Département"]
        station = row["station"]
        dates = row["Date_aaaammjj"]

        print(f"[{idx + 1}/{total}] Dépt {dept} | Station: {station} | Nbr dates: {len(dates)}")

        fichiers = charger_fichiers_meteo_du_departement(dept)
        df_meteo = extraire_donnees_station_dates(fichiers, station, dates)

        if not df_meteo.empty:
            df_meteo["DEPT"] = dept
            all_data.append(df_meteo)

    print("Fusion de toutes les données extraites...")
    if all_data:
        df_final = pd.concat(all_data, ignore_index=True)
        df_final.to_csv(FICHIER_SORTIE, sep=";", encoding="utf-8-sig", index=False)
        print(f"Fichier généré avec succès : {FICHIER_SORTIE} ({len(df_final)} lignes)")
    else:
        print("Aucune donnée météo extraite. Vérifie les fichiers source.")

if __name__ == "__main__":
    main()
