import pandas as pd

def ajouter_id_unique(input_file, output_file):
    # Lire le fichier CSV avec le bon séparateur et encodage
    df = pd.read_csv(input_file, sep=";", encoding="utf-8-sig")

    # Convertir la colonne "Date de première alerte" en datetime
    if 'Date de première alerte' in df.columns:
        df['Date de première alerte'] = pd.to_datetime(df['Date de première alerte'], errors='coerce', dayfirst=True)

    # Supprimer la colonne 'Numéro' si elle existe
    if 'Numéro' in df.columns:
        df = df.drop(columns=['Numéro'])

    # Créer une clé composite (commune + date-heure arrondie à l'heure)
    df['cle_temp'] = df['Nom de la commune'] + '_' + df['Date de première alerte'].dt.strftime('%Y-%m-%d %H:00')

    # Créer un dictionnaire pour mapper les clés aux IDs
    id_mapping = {cle: idx+1 for idx, cle in enumerate(df['cle_temp'].unique())}
    
    # Attribuer les IDs
    df['id'] = df['cle_temp'].map(id_mapping)
    
    # Supprimer la colonne temporaire
    df = df.drop(columns=['cle_temp'])
    
    # Réorganiser les colonnes pour mettre 'id' en première position
    cols = ['id'] + [col for col in df.columns if col != 'id']
    df = df[cols]

    # Sauvegarder le nouveau fichier avec le bon séparateur et encodage
    df.to_csv(output_file, sep=";", encoding="utf-8-sig", index=False)
    print(f"Fichier traité : {output_file}")


# Appels de la fonction (chemins inchangés)
ajouter_id_unique(
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_Nouvelle_Aquitaine.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\incendies\Incendies_Nouvelle_Aquitaine.csv"
)

ajouter_id_unique(
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\incendies\Incendies_PACA.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\incendies\Incendies_PACA.csv"
)