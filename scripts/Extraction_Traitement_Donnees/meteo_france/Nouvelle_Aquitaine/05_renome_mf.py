import pandas as pd
import os

fichier_meteo = r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\meteo_france\Nouvelle_Aquitaine\donnees_meteo_france_NA.csv"

renommage_colonnes = {
    # Identification et localisation
    "NUM_POSTE": "id_station",
    "NOM_USUEL": "nom_station",
    "LAT": "latitude",
    "LON": "longitude",
    "ALTI": "altitude_m",
    "AAAAMMJJHH": "date_heure",
    "DEPT": "departement",
    
    # Précipitations
    "RR1": "precipitations_1h_mm",
    "QRR1": "qualite_precipitations_1h",
    "DRR1": "duree_precipitations_min",
    "QDRR1": "qualite_duree_precipitations",
    
    # Vent à 10m
    "FF": "vent_moyen_10m_m_s",
    "QFF": "qualite_vent_moyen_10m",
    "DD": "direction_vent_moyen_10m_deg",
    "QDD": "qualite_direction_vent_moyen_10m",
    "FXY": "vent_max_heure_10m_m_s",
    "QFXY": "qualite_vent_max_heure_10m",
    "DXY": "direction_vent_max_heure_10m_deg",
    "QDXY": "qualite_direction_vent_max_heure_10m",
    "HXY": "heure_vent_max_heure",
    "QHXY": "qualite_heure_vent_max_heure",
    "FXI": "rafale_max_instantanee_10m_m_s",
    "QFXI": "qualite_rafale_max_instantanee_10m",
    "DXI": "direction_rafale_max_instantanee_10m_deg",
    "QDXI": "qualite_direction_rafale_max_instantanee_10m",
    "HXI": "heure_rafale_max_instantanee",
    "QHXI": "qualite_heure_rafale_max",
    
    # Vent à 2m
    "FF2": "vent_moyen_2m_m_s",
    "QFF2": "qualite_vent_moyen_2m",
    "DD2": "direction_vent_moyen_2m_deg",
    "QDD2": "qualite_direction_vent_moyen_2m",
    "FXI2": "rafale_max_instantanee_2m_m_s",
    "QFXI2": "qualite_rafale_max_instantanee_2m",
    "DXI2": "direction_rafale_max_instantanee_2m_deg",
    "QDXI2": "qualite_direction_rafale_max_instantanee_2m",
    "HXI2": "heure_rafale_max_instantanee_2m",
    "QHXI2": "qualite_heure_rafale_max_2m",
    
    # Vent moyenné sur 3 secondes
    "FXI3S": "rafale_max_3s_m_s",
    "QFXI3S": "qualite_rafale_max_3s",
    "DXI3S": "direction_rafale_max_3s_deg",
    "QDXI3S": "qualite_direction_rafale_max_3s",
    "HFXI3S": "heure_rafale_max_3s",
    "QHFXI3S": "qualite_heure_rafale_max_3s",
    
    # Températures
    "T": "temperature_air_c",
    "QT": "qualite_temperature_air",
    "TD": "point_de_rosee_c",
    "QTD": "qualite_point_de_rosee",
    "TN": "temperature_min_air_c",
    "QTN": "qualite_temperature_min_air",
    "HTN": "heure_temperature_min",
    "QHTN": "qualite_heure_temperature_min",
    "TX": "temperature_max_air_c",
    "QTX": "qualite_temperature_max_air",
    "HTX": "heure_temperature_max",
    "QHTX": "qualite_heure_temperature_max",
    "DG": "duree_gel_min",
    "QDG": "qualite_duree_gel",
    
    # Températures du sol
    "T10": "temperature_sol_10cm_c",
    "QT10": "qualite_temperature_sol_10cm",
    "T20": "temperature_sol_20cm_c",
    "QT20": "qualite_temperature_sol_20cm",
    "T50": "temperature_sol_50cm_c",
    "QT50": "qualite_temperature_sol_50cm",
    "T100": "temperature_sol_100cm_c",
    "QT100": "qualite_temperature_sol_100cm",
    "TNSOL": "temperature_min_surface_c",
    "QTNSOL": "qualite_temperature_min_surface",
    "TN50": "temperature_min_50cm_c",
    "QTN50": "qualite_temperature_min_50cm",
    "TCHAUSSEE": "temperature_chaussee_c",
    "QTCHAUSSEE": "qualite_temperature_chaussee",
    
    # Humidité
    "U": "humidite_relative_pourcent",
    "QU": "qualite_humidite_relative",
    "UN": "humidite_relative_min_pourcent",
    "QUN": "qualite_humidite_relative_min",
    "HUN": "heure_humidite_min",
    "QHUN": "qualite_heure_humidite_min",
    "UX": "humidite_relative_max_pourcent",
    "QUX": "qualite_humidite_relative_max",
    "HUX": "heure_humidite_max",
    "QHUX": "qualite_heure_humidite_max",
    "DHUMEC": "duree_humectation_min",
    "QDHUMEC": "qualite_duree_humectation",
    "DHUMI40": "duree_humidite_inf_40_pourcent_min",
    "QDHUMI40": "qualite_duree_humidite_inf_40",
    "DHUMI80": "duree_humidite_sup_80_pourcent_min",
    "QDHUMI80": "qualite_duree_humidite_sup_80",
    "TSV": "tension_vapeur_hpa",
    "QTSV": "qualite_tension_vapeur",
    
    # Pression
    "PMER": "pression_niveau_mer_hpa",
    "QPMER": "qualite_pression_mer",
    "PSTAT": "pression_station_hpa",
    "QPSTAT": "qualite_pression_station",
    "PMERMIN": "pression_mer_min_hpa",
    "QPMERMIN": "qualite_pression_mer_min",
    "GEOP": "geopotentiel_mgp",
    "QGEOP": "qualite_geopotentiel",
    
    # Nuages
    "N": "nebulosite_totale_octa",
    "QN": "qualite_nebulosite_totale",
    "NBAS": "nebulosite_couche_basse_octa",
    "QNBAS": "qualite_nebulosite_couche_basse",
    "CL": "code_synop_nuages_bas",
    "QCL": "qualite_code_synop_nuages_bas",
    "CM": "code_synop_nuages_moyens",
    "QCM": "qualite_code_synop_nuages_moyens",
    "CH": "code_synop_nuages_hauts",
    "QCH": "qualite_code_synop_nuages_hauts",
    
    # Couches nuageuses
    "N1": "nebulosite_couche_1_octa",
    "QN1": "qualite_nebulosite_couche_1",
    "C1": "type_nuage_couche_1",
    "QC1": "qualite_type_nuage_couche_1",
    "B1": "base_nuage_couche_1_m",
    "QB1": "qualite_base_nuage_couche_1",
    "N2": "nebulosite_couche_2_octa",
    "QN2": "qualite_nebulosite_couche_2",
    "C2": "type_nuage_couche_2",
    "QC2": "qualite_type_nuage_couche_2",
    "B2": "base_nuage_couche_2_m",
    "QB2": "qualite_base_nuage_couche_2",
    "N3": "nebulosite_couche_3_octa",
    "QN3": "qualite_nebulosite_couche_3",
    "C3": "type_nuage_couche_3",
    "QC3": "qualite_type_nuage_couche_3",
    "B3": "base_nuage_couche_3_m",
    "QB3": "qualite_base_nuage_couche_3",
    "N4": "nebulosite_couche_4_octa",
    "QN4": "qualite_nebulosite_couche_4",
    "C4": "type_nuage_couche_4",
    "QC4": "qualite_type_nuage_couche_4",
    "B4": "base_nuage_couche_4_m",
    "QB4": "qualite_base_nuage_couche_4",
    
    # Visibilité
    "VV": "visibilite_m",
    "QVV": "qualite_visibilite",
    "DVV200": "duree_visibilite_inf_200m_min",
    "QDVV200": "qualite_duree_visibilite_inf_200m",
    
    # Temps présent/passé
    "WW": "code_temps_present",
    "QWW": "qualite_code_temps_present",
    "W1": "code_temps_passe_1",
    "QW1": "qualite_code_temps_passe_1",
    "W2": "code_temps_passe_2",
    "QW2": "qualite_code_temps_passe_2",
    
    # Etat du sol
    "SOL": "etat_sol_sans_neige",
    "QSOL": "qualite_etat_sol_sans_neige",
    "SOLNG": "etat_sol_avec_neige",
    "QSOLNG": "qualite_etat_sol_avec_neige",
    
    # Données marines
    "TMER": "temperature_mer_c",
    "QTMER": "qualite_temperature_mer",
    "VVMER": "code_visibilite_mer",
    "QVVMER": "qualite_code_visibilite_mer",
    "ETATMER": "code_etat_mer",
    "QETATMER": "qualite_code_etat_mer",
    "DIRHOULE": "direction_houle_deg",
    "QDIRHOULE": "qualite_direction_houle",
    "HVAGUE": "hauteur_vague_m",
    "QHVAGUE": "qualite_hauteur_vague",
    "PVAGUE": "periode_vague_s",
    "QPVAGUE": "qualite_periode_vague",
    
    # Données nivologiques
    "HNEIGEF": "hauteur_neige_fraiche_6h_cm",
    "QHNEIGEF": "qualite_hauteur_neige_fraiche_6h",
    "NEIGETOT": "hauteur_neige_totale_cm",
    "QNEIGETOT": "qualite_hauteur_neige_totale",
    "TSNEIGE": "temperature_surface_neige_c",
    "QTSNEIGE": "qualite_temperature_surface_neige",
    "TUBENEIGE": "enfoncement_tube_neige_cm",
    "QTUBENEIGE": "qualite_enfoncement_tube_neige",
    "HNEIGEFI3": "hauteur_neige_fraiche_3h_cm",
    "QHNEIGEFI3": "qualite_hauteur_neige_fraiche_3h",
    "HNEIGEFI1": "hauteur_neige_fraiche_1h_cm",
    "QHNEIGEFI1": "qualite_hauteur_neige_fraiche_1h",
    "ESNEIGE": "code_etat_neige",
    "QESNEIGE": "qualite_code_etat_neige",
    "CHARGENEIGE": "charge_neige_kg_m2",
    "QCHARGENEIGE": "qualite_charge_neige",
    
    # Rayonnement
    "GLO": "rayonnement_global_utc_j_cm2",
    "QGLO": "qualite_rayonnement_global_utc",
    "GLO2": "rayonnement_global_tsv_j_cm2",
    "QGLO2": "qualite_rayonnement_global_tsv",
    "DIR": "rayonnement_direct_utc_j_cm2",
    "QDIR": "qualite_rayonnement_direct_utc",
    "DIR2": "rayonnement_direct_tsv_j_cm2",
    "QDIR2": "qualite_rayonnement_direct_tsv",
    "DIF": "rayonnement_diffus_utc_j_cm2",
    "QDIF": "qualite_rayonnement_diffus_utc",
    "DIF2": "rayonnement_diffus_tsv_j_cm2",
    "QDIF2": "qualite_rayonnement_diffus_tsv",
    "UV": "rayonnement_uv_utc_j_cm2",
    "QUV": "qualite_rayonnement_uv_utc",
    "UV2": "rayonnement_uv_tsv_j_cm2",
    "QUV2": "qualite_rayonnement_uv_tsv",
    "UV_INDICE": "indice_uv",
    "QUV_INDICE": "qualite_indice_uv",
    "INFRAR": "rayonnement_infrarouge_utc_j_cm2",
    "QINFRAR": "qualite_rayonnement_infrarouge_utc",
    "INFRAR2": "rayonnement_infrarouge_tsv_j_cm2",
    "QINFRAR2": "qualite_rayonnement_infrarouge_tsv",
    "INS": "insolation_utc_min",
    "QINS": "qualite_insolation_utc",
    "INS2": "insolation_tsv_min",
    "QINS2": "qualite_insolation_tsv",
    
    # Champs inutilisés
    "TLAGON": "champ_inutilise_1",
    "TVEGETAUX": "champ_inutilise_2",
    "ECOULEMENT": "champ_inutilise_3"
}

def renommer_colonnes_meteo(fichier):  
    if not os.path.exists(fichier):
        raise FileNotFoundError(f"Le fichier {fichier} n'existe pas")
    
    try:
        print(f"Lecture du fichier {fichier}...")
        df = pd.read_csv(fichier, sep=";", encoding="utf-8")

        colonnes_existantes = [col for col in renommage_colonnes if col in df.columns]
        print(f"{len(colonnes_existantes)} colonnes à renommer trouvées")

        df = df.rename(columns=renommage_colonnes)

        if "date_heure" in df.columns:
            df["date_heure"] = pd.to_datetime(
                df["date_heure"].astype(str), 
                format="%Y%m%d%H", 
                errors="coerce"
            )

        df.to_csv(fichier, sep=";", index=False, encoding="utf-8-sig")
        print("Mise à jour terminée avec succès")
        return True
    
    except Exception as e:
        print(f"Erreur lors du traitement: {str(e)}")
        return False

if __name__ == "__main__":
    renommer_colonnes_meteo(fichier_meteo)
