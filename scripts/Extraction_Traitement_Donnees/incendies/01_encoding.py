import pandas as pd
import os

def clean_csv(input_path, output_path, skiprows):
    try:
        df = pd.read_csv(input_path, sep=';', skiprows=skiprows, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(input_path, sep=';', skiprows=skiprows, encoding='windows-1252')

    # Nettoyer les espaces dans les noms de colonnes et dans les données string
    df.columns = df.columns.str.strip()
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Sauvegarder le fichier nettoyé
    df.to_csv(
        output_path,
        sep=';',
        index=False,
        encoding='utf-8-sig',
        lineterminator='\n'
    )
    print(f"Fichier nettoyé et sauvegardé sous : {output_path}")

# Chemins complets des fichiers à traiter
input_files = {
    "Nouvelle_Aquitaine": {
        "input": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\incendies\Incendies_Nouvelle_Aquitaine.csv",
        "skiprows": 6,
        "output": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_Nouvelle_Aquitaine.csv"
    },
    "PACA": {
        "input": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\incendies\Incendies_PACA.csv",
        "skiprows": 3,
        "output": r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_PACA.csv"
    }
}

# Assure-toi que le dossier de sortie existe
output_dir = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies"
os.makedirs(output_dir, exist_ok=True)

# Traitement des deux fichiers
for region, paths in input_files.items():
    clean_csv(paths["input"], paths["output"], paths["skiprows"])
