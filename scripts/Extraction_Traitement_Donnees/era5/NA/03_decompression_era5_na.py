import os
import zipfile
import shutil
import xarray as xr
import pandas as pd

# === PARAMÈTRES ===
DOSSIER_RACINE = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\data\era5\NA"
DOSSIER_OUTPUT = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\ERA5\Nouvelle_Aquitaine"
SEPARATEUR_CSV = ";"

VARIABLES_METEO = ["t2m", "tp", "swvl1", "ssrd", "pev", "u10", "v10", "lai_hv"]


def creer_dossier_si_absent(path):
    os.makedirs(path, exist_ok=True)


def est_un_fichier_zip_valide(chemin_fichier):
    return zipfile.is_zipfile(chemin_fichier)


def decompresser_fichier(chemin_fichier, dossier_output):
    try:
        with zipfile.ZipFile(chemin_fichier, "r") as zipf:
            for nom in zipf.namelist():
                if nom.endswith(".nc"):
                    # Utiliser le nom du fichier original pour le nom décompressé
                    nom_decompresse = os.path.basename(chemin_fichier).replace(".nc", "_decompressed.nc")
                    chemin_decompresse = os.path.join(dossier_output, nom_decompresse)

                    creer_dossier_si_absent(dossier_output)
                    with zipf.open(nom) as src, open(chemin_decompresse, "wb") as dst:
                        shutil.copyfileobj(src, dst)

                    print(f" Décompressé : {nom_decompresse}")
                    return chemin_decompresse
    except Exception as e:
        print(f"ERREUR Décompression : {chemin_fichier} -> {e}")
    return None


def convertir_nc_en_csv(chemin_nc, dossier_output):
    try:
        with xr.open_dataset(chemin_nc) as ds:
            df = pd.DataFrame()
            df["datetime"] = ds["valid_time"].values

            for var in VARIABLES_METEO:
                df[var] = ds[var].mean(dim=("latitude", "longitude")).values if var in ds else None

            df["lat"] = float(ds.latitude.values.mean())
            df["lon"] = float(ds.longitude.values.mean())

            nom_csv = os.path.basename(chemin_nc).replace("_decompressed.nc", ".csv")
            chemin_csv = os.path.join(dossier_output, nom_csv)
            creer_dossier_si_absent(dossier_output)
            df.to_csv(chemin_csv, index=False, sep=SEPARATEUR_CSV, encoding="utf-8-sig")

            print(f"CSV généré : {os.path.basename(chemin_csv)}")
            return True
    except Exception as e:
        print(f"ERREUR Conversion : {chemin_nc} -> {e}")
    return False


def traitement_global(dossier_base, dossier_output):
    print(f"\n--- TRAITEMENT GLOBAL DANS : {dossier_base} ---")
    total = 0

    for racine, _, fichiers in os.walk(dossier_base):
        for fichier in fichiers:
            chemin_complet = os.path.join(racine, fichier)

            # Vérifier si le fichier est un .nc qui est en réalité un .zip
            if fichier.endswith(".nc") and est_un_fichier_zip_valide(chemin_complet):
                chemin_nc_decompresse = decompresser_fichier(chemin_complet, dossier_output)
                if chemin_nc_decompresse and convertir_nc_en_csv(chemin_nc_decompresse, dossier_output):
                    total += 1
            # Vérifier si le fichier est déjà décompressé et prêt à être converti
            elif fichier.endswith("_decompressed.nc"):
                if convertir_nc_en_csv(chemin_complet, dossier_output):
                    total += 1

    print(f"\n--- TERMINÉ : {total} fichiers traités ---")


# === EXÉCUTION ===
if __name__ == "__main__":
    traitement_global(DOSSIER_RACINE, DOSSIER_OUTPUT)


