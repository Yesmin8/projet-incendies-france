# Analyse des Incendies de Forêt en Nouvelle-Aquitaine et PACA
## Objectif

Ce projet vise à analyser l’influence des conditions météorologiques sur les incendies de forêt dans deux régions particulièrement exposées : Nouvelle-Aquitaine et Provence-Alpes-Côte d’Azur (PACA).

En croisant des données d’incendies (base BDIFF) avec des observations climatiques (Météo-France) et des données issues de la réanalyse ERA5 (Copernicus), l’objectif est d’identifier les conditions propices aux départs de feu, en vue d’améliorer la prévention et la modélisation du risque incendie.

## Structure du projet
``` bash
projet_incendies/
├── data/
│   ├── meteo_france/
│   │   ├── NA/
│   │   └── PACA/
│   ├── incendies/
│   │   ├── codes-postaux/
│   │   ├── Incendies_NA.csv
│   │   └── Incendies_PACA.csv
│   └── era5/
│       ├── NA/
│       └── PACA/
│
├── notebooks/
│   ├── 01_preprocess_era5.ipynb
│   ├── 01_preprocess_incendies.ipynb
│   ├── 01_preprocess_meteo_france.ipynb
│   ├── 02_analyse_descriptive_era5.ipynb
│   ├── 02_analyse_descriptive_incendies.ipynb
│   └── 02_analyse_descriptive_meteo_france.ipynb
│
├── outputs/
│   ├── intermediaires/
│   │   ├── meteo_france/
│   │   ├── incendies/
│   │   ├── era5/
│   │   └── analyse/
│   └── final/
│       ├── incendies/
│       ├── meteo_france/
│       └── era5/
│
└── scripts/
    └── Extraction_Traitement_Donnees/
        ├── era5/
        │   ├── NA/
        │   │   ├── 01_telechargement_era5_na_.py
        │   │   ├── 02_organiser_fichiers_nc_par_annee.py
        │   │   ├── 03_decompression_era5_na.py
        │   │   └── 04_donnees_meteo_combinees.py
        │   ├── PACA/
        │   │   ├── 01_telechargement_era5_paca_.py
        │   │   ├── 02_organiser_fichiers_paca_par_annee.py
        │   │   ├── 03_decompression_era5_paca.py
        │   │   └── 04_donnees_meteo_combinees.py
        │   └── 05_id.py
        ├── incendies/
        │   ├── 01_encoding.py
        │   ├── 02_Lang_Amp_na.py
        │   ├── 02_Lang_Amp_paca.py
        │   ├── 03_finally_na.py
        │   ├── 03_finally_paca.py
        │   ├── 04_station.py
        │   └── 05_id.py
        └── meteo_france/
            ├── Nouvelle_Aquitaine/
            │   ├── 01_convertisseur_csv_NA.py
            │   ├── 02_preprocess_incendies_NA.py
            │   ├── 03_extract_NA.py
            │   ├── 04_filtrée.py
            │   └── 05_renome_mf.py
            └── PACA/
                ├── 01_convertisseur_csv_PACA.py
                ├── 02_preprocess_incendies_PACA.py
                ├── 03_extract_PACA.py
                ├── 04_filtrée.py
                ├── 05_renome_mf.py
                └── id.py
```
## Sources de données et traitements

### Données d'incendies (BDIFF)

- **Source principale** : [BDIFF – Base de Données des Incendies de Forêt](https://www.promethee.fr/)
- **Contenu** : Données détaillées des feux de forêt en PACA et NA
- **Traitement** :
  - nettoyage initale (séparateurs sep=';', encodage encoding='utf-8-sig')
  - Complétion des coordonnées géographiques via :
    - [Base officielle des codes postaux – Datanova](https://datanova.laposte.fr)
    - [API Adresse - data.gouv.fr](https://api-adresse.data.gouv.fr)
    - Gestion manuelle des communes non trouvées en raison de changements gouvernementaux (fichiers Communes_non_trouvees_*.xlsx).
  
### Météo France

- **Source** : [meteo.data.gouv.fr](https://meteo.data.gouv.fr/datasets/6569b4473bedf2e7abad3b72)
- **Contenu** : Observations horaires par station (2010–2025)
- **Traitement** :
  - Association de chaque incendie à la station la plus proche grâce aux données géologiques et aux départements (script 04_station.py).
  - Extraction des observations uniquement aux dates des incendies
  - Renommage des colonnes techniques selon la documentation officielle
  - Ajout d’un identifiant unique id_incendie pour la liaison des données
  - 
### ERA5 (Copernicus)

- **Source** : [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
- **Format** : .nc (NetCDF, compressé)
- **Spécificités** :
  - Données horaires très détaillées
  - Ciblage sur les 15 mois les plus destructeurs
  - Extraction limitée à 3 heures clés pour chaque incendie (t−1h, t, t+1h)
  - Variables sélectionnées : 't2m', 'tp', 'swvl1', 'ssrd', 'pev', 'u10', 'v10', 'lai_hv'
- **Traitement** :
  - Décompression des fichiers .nc
  - Extraction et conversion vers .csv
  - Concaténation par région
    
---
## Pipeline de traitement

### Prétraitement

- Nettoyage des données brutes (incendies et météo)
- Conversion des fichiers .nc en .csv
- Enrichissement géographique (coordonnées, codes INSEE)
- Association incendie ↔ station météo
  
### Fusion & structuration

- Création d’un identifiant unique id_incendie pour relier les sources
- Harmonisation des formats (dates, noms, unités)
- Centralisation des jeux de données finaux par région/source

## Analyse descriptive 
#### Notebooks principaux
Après avoir effectué tous les traitements nécessaires dans scripts, nous avons commencé l’exploration de la qualité des données et des paramètres influençant les incendies.  
Dans les fichiers `01_preprocess_*.ipynb`, nous avons préparé et nettoyé les données issues de Météo France, ERA5 et des bases d’incendies.  
Ensuite, dans les fichiers `02_analyse_descriptive_*.ipynb`, nous avons réalisé l’analyse descriptive complète de l’ensemble des paramètres pertinents.  

Toutes les analyses et descriptions sont détaillées et présentes dans les notebooks, qui sont bien commentés et organisés :  
- `01_preprocess_*.ipynb` : traitement initial des données brutes  
- `02_analyse_descriptive_*.ipynb` : statistiques, graphiques, visualisations  

Les résultats sont organisés dans le dossier `outputs/` :  
- `outputs/intermediaires/Analyse/` : toutes les analyses utilisées dans le prétraitement, les dataframes et heatmaps nettoyés sont sauvegardés ici pour une utilisation ultérieure dans l'analyse descriptive  
- `outputs/intermediaires/Analyse/graphe_analyse_descriptive/` : visualisations par source et région des résultats des fichiers d’analyse descriptive  

---

## Installation et configuration

pour telecharger les données de era5 depuis [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
1. Créez un compte Copernicus.
2. Récupérez votre clé API.
3. Ajoutez un fichier .cdsapirc dans votre dossier personnel (C:) contenant :
``` bash
url: https://cds.climate.copernicus.eu/api/v2
key: votre-identifiant:clé-secrète
```
concernant l'api [API Adresse - data.gouv.fr](https://api-adresse.data.gouv.fr), elle est accessible directement sans besoin de clé.
```bash
git clone https://github.com/ton-compte/projet_incendies.git
cd projet_incendies
pip install -r requirements.txt
```

## Contraintes techniques & choix méthodologiques

L’intégration des données météorologiques a soulevé plusieurs défis techniques, en particulier en ce qui concerne la qualité, le volume et la structure des sources disponibles :

### Qualité variable des données Météo-France

- Les fichiers d’observations horaires de Météo-France affichent un taux élevé de valeurs manquantes pour certaines stations et paramètres.
- Un travail d’analyse de complétude a été réalisé pour sélectionner les variables exploitables (température, humidité relative, vent, etc.).
- Les jeux de données ont été limités aux journées contenant des incendies, afin d’optimiser le traitement et réduire les biais liés aux valeurs manquantes.

### Téléchargement intensif des données ERA5

Bien que très complètes, les données ERA5 sont longues à télécharger via l’API Copernicus.

Pour chaque incendie, nous avons ciblé uniquement 3 heures précises :
- Heure de l’incendie (t)
- Heure précédente (t−1h)
- Heure suivante (t+1h)

Et uniquement les 8 variables les plus corrélées au risque d’incendie :
- Température de l’air (t2m)
- Précipitations (tp)
- Humidité du sol (swvl1)
- Rayonnement solaire (ssrd)
- Évaporation potentielle (pev)
- Vent zonal (u10) et méridien (v10)
- Indice de feuillage (lai_hv)

Malgré ce ciblage, le téléchargement reste très long : il faut entre 5 et 6 jours continus pour traiter chaque région (Nouvelle-Aquitaine et PACA) pour l’ensemble des incendies.

#### Stratégie adoptée

Face à ces contraintes :
- Une extraction exhaustive a été réalisée pour les 15 mois les plus dévastateurs (en surface brûlée), représentant un échantillon significatif des conditions extrêmes.
- Les fichiers téléchargés au format .nc peuvent prêter à confusion, car ils sont initialement compressés. Malheureusement, cette information n'est pas indiquée dans la documentation ni dans le format lui-même, ce qui peut entraîner des malentendus. Par conséquent, ces fichiers nécessitent une phase de décompression et puis de conversion avant d'être exploités (03_decompression_era5_na.py, 03_decompression_era5_paca.py)
- Les fichiers .csv.gz de Météo-France ont, à l’inverse, été plus simples à intégrer grâce à un simple script de conversion automatique.

## Perspectives et travaux futurs

Ce travail constitue une étape majeure dans la compréhension des dynamiques des incendies de forêt en Nouvelle-Aquitaine et PACA.  
Les analyses descriptives détaillées et la structuration rigoureuse des données offrent une base solide et fiable pour approfondir la connaissance des facteurs influents.  

Dans les phases suivantes, le projet s’orientera vers :  
- Le développement de modèles prédictifs intégrant les variables climatiques et environnementales identifiées  
- L’analyse spatiale fine et la cartographie dynamique des risques  
- L’étude des interactions entre facteurs anthropiques et naturels  
- L’évaluation de scénarios climatiques futurs pour anticiper les évolutions du risque incendie  

Cette démarche progressive vise à enrichir la précision des outils de prévention et à soutenir la prise de décision opérationnelle, contribuant ainsi à une meilleure gestion durable des territoires exposés.  
Le travail réalisé jusqu’ici constitue donc une base solide, mais la richesse et la complexité du phénomène incendie appellent à des analyses complémentaires et à une évolution continue du projet.

---
