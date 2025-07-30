import pandas as pd

# Fichiers
INPUT_CSV = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_Nouvelle_Aquitaine.csv"
CORRECTIONS_XLSX = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\incendies\codes-postaux\Communes_non_trouvees_NA.xlsx"
OUTPUT_CSV = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_Nouvelle_Aquitaine.csv"

# Charger les données
df = pd.read_csv(INPUT_CSV, sep=';', encoding='utf-8-sig')
corrections = pd.read_excel(CORRECTIONS_XLSX)

# Nettoyage des colonnes
df.columns = df.columns.str.strip()
corrections.columns = corrections.columns.str.strip()

# Forcer le format INSEE à 5 chiffres
df["Code INSEE"] = df["Code INSEE"].apply(lambda x: str(x).zfill(5))
corrections["Code INSEE"] = corrections["Code INSEE"].astype(str).str.zfill(5)

# Appliquer toutes les corrections (lat, lon, éventuellement nom INSEE corrigé)
for _, row in corrections.iterrows():
    insee = row["Code INSEE"]
    commune = row["Commune"]
    lat = row.get("latitude", None)
    lon = row.get("longitude", None)

    condition = df["Code INSEE"] == insee

    if not condition.any():
        print(f"Aucune ligne trouvée avec Code INSEE = {insee} → Ignoré")
        continue

    if pd.notna(commune):
        df.loc[condition, "Nom de la commune"] = commune
    if pd.notna(lat):
        df.loc[condition, "latitude"] = lat
    if pd.notna(lon):
        df.loc[condition, "longitude"] = lon

    print(f"Mise à jour pour {commune or 'Code INSEE'} ({insee})")

# Sauvegarde finale
df.to_csv(OUTPUT_CSV, sep=';', index=False, encoding='utf-8-sig')
print(f"\nCorrections manuelles intégrées dans : {OUTPUT_CSV}")
