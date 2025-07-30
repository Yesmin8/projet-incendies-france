import pandas as pd
import cdsapi
import time
from datetime import timedelta
import os

# --- Nouveau dossier de sortie ---
OUTPUT_DIR = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\era5\NA"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chargement des données
df = pd.read_csv(
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_Nouvelle_Aquitaine.csv", 
    sep=';'
)
df.columns = df.columns.str.strip()
df["Date de première alerte"] = pd.to_datetime(df["Date de première alerte"], dayfirst=True, errors='coerce')
df["Surface parcourue (m2)"] = pd.to_numeric(df["Surface parcourue (m2)"], errors='coerce').fillna(0)
df = df.dropna(subset=["latitude", "longitude", "Date de première alerte"])

# Identifier les 15 mois les plus destructeurs
df["Année"] = df["Date de première alerte"].dt.year
df["Mois"] = df["Date de première alerte"].dt.month

top_months = (
    df.groupby(["Année", "Mois"])["Surface parcourue (m2)"]
    .sum()
    .reset_index()
    .sort_values(by="Surface parcourue (m2)", ascending=False)
    .head(15)
)

top_months_set = set((row["Année"], row["Mois"]) for _, row in top_months.iterrows())

# Filtrer les incendies
df_filtered = df[df.apply(lambda x: (x["Année"], x["Mois"]) in top_months_set, axis=1)]

# Variables météo
variables = [
    '2m_temperature',
    'total_precipitation',
    'volumetric_soil_water_layer_1',
    'surface_solar_radiation_downwards',
    'potential_evaporation',
    '10m_u_component_of_wind',
    '10m_v_component_of_wind',
    'leaf_area_index_high_vegetation'
]

client = cdsapi.Client()

# Boucle téléchargement
for idx, row in df_filtered.iterrows():
    date = row["Date de première alerte"]
    lat = float(row["latitude"])
    lon = float(row["longitude"])

    year = str(date.year)
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"

    heure = date.hour
    heures = sorted(set([max(0, heure - 1), heure, min(23, heure + 1)]))
    heures_str = [f"{h:02d}:00" for h in heures]

    north = round(lat + 0.05, 2)
    south = round(lat - 0.05, 2)
    west = round(lon - 0.05, 2)
    east = round(lon + 0.05, 2)

    filename = f"meteo_{lat:.4f}_{lon:.4f}_{year}-{month}-{day}.nc"
    filepath = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(filepath):
        print(f"Fichier déjà existant, on saute : {filepath}")
        continue

    print(f"\nTéléchargement : {filename} | Heures : {heures_str} | Zone : N={north}, W={west}, S={south}, E={east}")

    try:
        client.retrieve(
            "reanalysis-era5-land",
            {
                "variable": variables,
                "year": year,
                "month": [month],
                "day": [day],
                "time": heures_str,
                "format": "netcdf",
                "area": [north, west, south, east],
            },
            filepath
        )
    except Exception as e:
        print(f"Erreur lors du téléchargement de {filename} : {e}")

    time.sleep(1)
