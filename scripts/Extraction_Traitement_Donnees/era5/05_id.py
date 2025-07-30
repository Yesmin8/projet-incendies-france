import pandas as pd
from datetime import timedelta

def match_fires_weather(weather_file, fires_file, output_file):
    # Charger les fichiers CSV
    df_weather = pd.read_csv(weather_file, sep=";")
    df_fires = pd.read_csv(fires_file, sep=";")

    # Convertir les colonnes de date/heure au format datetime
    df_weather["datetime"] = pd.to_datetime(df_weather["datetime"])
    df_fires["Date de première alerte"] = pd.to_datetime(df_fires["Date de première alerte"])

    # Créer une copie du DataFrame météo pour stocker les correspondances
    # Cela permet de s\'assurer que chaque ligne météo est associée au meilleur incendie correspondant.
    df_weather_matched = df_weather.copy()
    df_weather_matched["id_incendie"] = None
    df_weather_matched["time_diff_seconds"] = float("inf") # Pour stocker la différence de temps en secondes

    # Itérer sur chaque ligne du DataFrame des incendies
    for index_fire, fire_row in df_fires.iterrows():
        fire_datetime = fire_row["Date de première alerte"]
        fire_date = fire_datetime.date()
        fire_hour = fire_datetime.hour
        fire_lat = fire_row["latitude"]
        fire_lon = fire_row["longitude"]
        fire_id = fire_row["id"]

        # Filtrer les données météo par date exacte
        df_weather_filtered_date = df_weather[df_weather["datetime"].dt.date == fire_date]

        if not df_weather_filtered_date.empty:
            # Définir l\'intervalle de temps (±1 heure sur les heures pleines)
            # Calculer les heures pleines à considérer
            valid_hours = set()
            valid_hours.add(fire_hour)
            valid_hours.add((fire_hour - 1 + 24) % 24)
            valid_hours.add((fire_hour + 1) % 24)

            # Filtrer par heure
            df_weather_filtered_time = df_weather_filtered_date[df_weather_filtered_date["datetime"].dt.hour.isin(valid_hours)]

            if not df_weather_filtered_time.empty:
                # Calculer la distance géographique (tolérance de 0.1 degré)
                tolerance = 0.1

                for index_weather, weather_row in df_weather_filtered_time.iterrows():
                    weather_lat = weather_row["lat"]
                    weather_lon = weather_row["lon"]

                    distance = ((weather_lat - fire_lat)**2 + (weather_lon - fire_lon)**2)**0.5

                    if distance <= tolerance:
                        # Calculer la différence de temps absolue en secondes
                        time_diff = abs((weather_row["datetime"] - fire_datetime).total_seconds())

                        # Si cette correspondance est meilleure que la précédente pour cette ligne météo
                        if time_diff < df_weather_matched.loc[index_weather, "time_diff_seconds"]:
                            df_weather_matched.loc[index_weather, "id_incendie"] = fire_id
                            df_weather_matched.loc[index_weather, "time_diff_seconds"] = time_diff

    # Supprimer la colonne temporaire
    df_weather_matched = df_weather_matched.drop(columns=["time_diff_seconds"])

    # Réorganiser les colonnes pour mettre 'id_incendie' en première position
    cols = ["id_incendie"] + [col for col in df_weather_matched.columns if col != "id_incendie"]
    df_weather_matched = df_weather_matched[cols]

    # Sauvegarder le DataFrame météo mis à jour
    df_weather_matched.to_csv(output_file, sep=";", index=False)
    print(f"Fichier mis à jour sauvegardé sous : {output_file}")

match_fires_weather(
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\ERA5\donnees_meteo_combinees_NA.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\incendies\Incendies_Nouvelle_Aquitaine.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\ERA5\donnees_meteo_ERA5_NA.csv"
)

match_fires_weather(
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\intermediaires\ERA5\donnees_meteo_combinees_PACA.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\incendies\Incendies_PACA.csv",
    r"C:\Users\User\OneDrive - Ministere de l'Enseignement Superieur et de la Recherche Scientifique\projet_incendies\outputs\final\ERA5\donnees_meteo_ERA5_PACA.csv"
)