import pandas as pd

# Charger le fichier existant
df = pd.read_csv(r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\PACA\donnees_meteo_france_PACA.csv", sep=";", encoding="utf-8-sig")

# Mettre la colonne DEPT en première position
cols = df.columns.tolist()
cols.insert(0, cols.pop(cols.index("DEPT")))
df = df[cols]

# Trier par DEPT, NOM_USUEL, AAAAMMJJHH en ordre croissant (mois 1 → 12, années croissantes)
df = df.sort_values(by=["DEPT", "NOM_USUEL", "AAAAMMJJHH"], ascending=[True, True, True])

# Réécrire le fichier existant avec les modifications
df.to_csv("meteo_incendies_filtrée.csv", sep=";", encoding="utf-8-sig", index=False)

print("Modifications appliquées avec succès au fichier existant.")
