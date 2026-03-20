<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AWS-Cloud-232F3E?style=flat&logo=amazonaws&logoColor=white" alt="AWS">
  <img src="https://img.shields.io/badge/Pandas-2.2-150458?style=flat&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Selenium-4.16-43B02A?style=flat&logo=selenium&logoColor=white" alt="Selenium">
  <img src="https://img.shields.io/badge/Plotly-5.18-3F4F75?style=flat&logo=plotly&logoColor=white" alt="Plotly">
</p>

# Projet Kayak - Recommandation de destinations de voyage

Pipeline Data Engineering End-to-End pour identifier les meilleures destinations en France selon la météo et les hôtels disponibles.

## About

Ce projet répond à la question : "Où partir et où dormir pour profiter du meilleur climat cette semaine ?"

Le système collecte des données météo et hôtelières, les stocke dans le Cloud AWS, puis génère des cartes interactives de recommandation. Le pipeline complet s'exécute via 6 notebooks séquentiels ou via le script `main.py`.

## Dataset

Les données proviennent de trois sources :

- **Nominatim (OpenStreetMap)** : coordonnées GPS des 35 villes cibles
- **OpenWeatherMap One Call 3.0** : prévisions météo à 7 jours (température, pluie)
- **Booking.com (scraping Selenium)** : top 20 hôtels par ville (nom, note, description, lien)

Les CSV générés sont envoyés vers AWS S3 (Data Lake) puis chargés dans PostgreSQL via AWS RDS (Data Warehouse).

## Installation

```bash
git clone https://github.com/athanormark/KAYAK-_-BLOC-1_JEDHA_FORMATION.git
cd KAYAK-_-BLOC-1_JEDHA_FORMATION
pip install -r requirements.txt
```

Copiez `.env.example` vers `.env` et renseignez vos clés :

```bash
cp .env.example .env
```

## Pipeline

| Notebook | Description |
|---|---|
| `01_Cities_list.ipynb` | Géolocalisation GPS des 35 villes via API Nominatim |
| `02_Meteo_call.ipynb` | Prévisions météo 7 jours via OpenWeatherMap |
| `03_Booking_Scraping.ipynb` | Scraping des hôtels sur Booking.com (Selenium headless) |
| `04_Upload_S3.ipynb` | Upload des CSV vers le Data Lake AWS S3 |
| `05_SQL_RDS.ipynb` | ETL complet : S3 vers PostgreSQL RDS |
| `06_Plotly_Viz.ipynb` | Cartes interactives (Top 5 destinations + Top 20 hôtels) |

Exécution automatisée du pipeline complet :

```bash
python main.py
```

Architecture : API/Scraping -> Python (Pandas) -> CSV -> AWS S3 (Data Lake) -> ETL -> AWS RDS (Data Warehouse) -> Plotly

## Résultats

Les cartes ci-dessous sont générées à partir des données du 07/03/2026. Les résultats varient selon la date d'exécution car les prévisions météo sont en temps réel.

**Carte 1 : Top 5 Destinations (score météo)**

Classement par score composite : `temperature_moyenne - (pluie_totale x 0.15)`

![Top 5 Destinations](maps/top5_destinations.png)

**Carte 2 : Top 20 Hôtels**

Meilleurs établissements (par note Booking) situés dans les 5 zones recommandées.

![Top 20 Hotels](maps/top20_hotels.png)

## Deploiement AWS

Les donnees sont hebergees dans le Cloud AWS (region eu-west-3 Paris).

**Console AWS S3 - Data Lake**

![Compartiment S3](screenshots/Compartiment%20S3.png)

**Contenu du bucket (fichiers CSV)**

![Fichiers CSV dans S3](screenshots/Compartiment%20S3%20-%20DOC%20CSV.png)

**Apercu des fichiers uploades**

| Fichier | Capture |
|---|---|
| `cities_coordinates.csv` | ![cities_coordinates](screenshots/cities_coordinates_S3.png) |
| `cities_weather_data_7days.csv` | ![weather_data](screenshots/cities_weather_data_7days_S3.png) |
| `hotels_data.csv` | ![hotels_data](screenshots/hotels_data_S3.png) |

## Structure du projet

```text
.
├── 01_Cities_list.ipynb        # Géolocalisation
├── 02_Meteo_call.ipynb         # API Météo
├── 03_Booking_Scraping.ipynb   # Scraping Booking
├── 04_Upload_S3.ipynb          # Upload S3
├── 05_SQL_RDS.ipynb            # ETL vers RDS
├── 06_Plotly_Viz.ipynb         # Visualisation
├── main.py                     # Orchestrateur du pipeline
├── requirements.txt            # Dépendances Python
├── .env.example                # Template des variables d'environnement
├── .gitignore
├── maps/                       # Screenshots des cartes Plotly
├── screenshots/                # Captures AWS (S3, RDS)
└── README.md
```

## Auteur

Athanor SAVOUILLAN · [GitHub](https://github.com/athanormark)
