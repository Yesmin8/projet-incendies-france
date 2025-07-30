import pandas as pd
import requests
import time

# Fichiers
INCENDIES_CSV = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_PACA.csv"
GEOLOC_CSV = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\incendies\codes-postaux\base-officielle-codes-postaux-PACA.csv"
NOT_FOUND_XLSX = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\incendies\codes-postaux\Communes_non_trouvees_PACA.xlsx"
OUTPUT_CSV = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_PACA.csv"

# Départements PACA
PACA_DEPARTMENTS = {"04", "05", "06", "13", "83", "84"}

# --- Étape 1 : Fusion initiale avec le fichier géoloc CSV ---
df_incendies = pd.read_csv(INCENDIES_CSV, sep=';', encoding='utf-8-sig')
df_geoloc = pd.read_csv(GEOLOC_CSV, sep=',')

# Nettoyage
df_incendies.columns = df_incendies.columns.str.strip()
df_geoloc.columns = df_geoloc.columns.str.strip()

# Format INSEE
df_incendies["Code INSEE"] = df_incendies["Code INSEE"].apply(lambda x: str(int(x)).zfill(5))
df_geoloc["code_commune_insee"] = df_geoloc["code_commune_insee"].apply(lambda x: str(x).zfill(5))

# Garder uniquement les colonnes utiles
df_geoloc_reduit = df_geoloc[["code_commune_insee", "latitude", "longitude"]].drop_duplicates(subset="code_commune_insee")

# Fusion
df = pd.merge(df_incendies, df_geoloc_reduit, left_on="Code INSEE", right_on="code_commune_insee", how="left")
df.drop(columns=["code_commune_insee"], inplace=True)

# --- Étape 2 : Complément via l’API pour les communes manquantes ---
missing = df[df["latitude"].isna() | df["longitude"].isna()]
communes_uniques = missing[["Nom de la commune", "Code INSEE"]].drop_duplicates()

coord_dict = {}
not_found = {}

def get_coordinates_ban(commune, insee_code):
    query = f"{commune} {insee_code[:2]}"
    url = f"https://api-adresse.data.gouv.fr/search/?q={query}&limit=50"
    try:
        response = requests.get(url)
        data = response.json()
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            context = props.get("context", "")
            citycode = props.get("citycode")
            if citycode == insee_code and any(dep + "," in context for dep in PACA_DEPARTMENTS):
                lon, lat = feature["geometry"]["coordinates"]
                return lat, lon
    except Exception as e:
        print(f"Erreur API pour {commune} ({insee_code}) : {e}")
    return None, None

for _, row in communes_uniques.iterrows():
    commune = row["Nom de la commune"]
    insee = row["Code INSEE"]

    lat, lon = get_coordinates_ban(commune, insee)
    if lat and lon:
        coord_dict[(commune, insee)] = (lat, lon)
        print(f"{commune} ({insee}) → lat: {lat}, lon: {lon}")
    else:
        not_found[(commune, insee)] = None
        print(f"Introuvable : {commune} ({insee})")

    time.sleep(1)  # respecter l’API gratuite

# Appliquer les coordonnées trouvées à toutes les lignes concernées
for (commune, insee), (lat, lon) in coord_dict.items():
    df.loc[(df["Nom de la commune"] == commune) & (df["Code INSEE"] == insee), "latitude"] = lat
    df.loc[(df["Nom de la commune"] == commune) & (df["Code INSEE"] == insee), "longitude"] = lon

# --- Étape 3 : Sauvegardes finales ---
df.to_csv(OUTPUT_CSV, sep=';', index=False, encoding='utf-8-sig')
print(f"\nFichier final enrichi exporté : {OUTPUT_CSV}")

# Exporter les communes non trouvées dans un fichier Excel
if not_found:
    not_found_df = pd.DataFrame([(commune, insee) for (commune, insee) in not_found], columns=["Commune", "Code INSEE"])
    not_found_df.to_excel(NOT_FOUND_XLSX, index=False)
    print(f"Liste des communes non trouvées exportée dans : {NOT_FOUND_XLSX}")
