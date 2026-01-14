# ✈️ Projet Kayak - Moteur de Recommandation de Voyage

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-232F3E?logo=amazon-aws&logoColor=white)
![S3](https://img.shields.io/badge/AWS_S3-Data_Lake-569A31?logo=amazons3&logoColor=white)
![RDS](https://img.shields.io/badge/AWS_RDS-PostgreSQL-527FFF?logo=postgresql&logoColor=white)
![Libs](https://img.shields.io/badge/Lib-Pandas_|_Requests_|_SQLAlchemy-orange)
![Viz](https://img.shields.io/badge/Viz-Plotly-3F4F75?logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📋 Vue d'ensemble
Ce projet est un pipeline de **Data Engineering End-to-End** conçu pour recommander les meilleures destinations de voyage en France.

Il répond à la question : *"Où aller et où dormir pour profiter du meilleur climat cette semaine ?"*

Le système automatise 4 étapes clés :
1.  **Collecte (ETL) :** Récupération de données via API (Météo) et Scraping (Booking.com).
2.  **Stockage (Data Lake) :** Sauvegarde des données brutes sur **AWS S3**.
3.  **Structuration (Data Warehouse) :** Nettoyage et chargement dans une base SQL sur **AWS RDS**.
4.  **Visualisation :** Génération de cartes interactives pour l'aide à la décision.

## 🏗️ Architecture Technique

> **Flux de données :**
> API/Scraping ➔ Python (Pandas) ➔ Fichiers CSV ➔ **AWS S3** ➔ **AWS RDS (SQL)** ➔ Dashboard Plotly

## 🚀 Installation et Exécution

### 1. Cloner le projet
```bash
git clone [https://github.com/athanormark/KAYAK-_-BLOC-1_JEDHA_FORMATION.git](https://github.com/athanormark/KAYAK-_-BLOC-1_JEDHA_FORMATION.git)
cd KAYAK-_-BLOC-1_JEDHA_FORMATION
```

## 📋 Vue d'ensemble
Ce projet est un pipeline de Data Engineering complet conçu pour recommander les meilleures destinations de voyage en France, en se basant sur les prévisions météorologiques et la qualité des hôtels.

Il reproduit le fonctionnement d'un comparateur de voyage type "Kayak" à travers 4 étapes clés :
1.  **Collecte (Extract) :** Récupération de données via API (Météo) et Scraping Web (Booking.com).
2.  **Stockage (Load) :** Sauvegarde sécurisée des données brutes dans un Data Lake (AWS S3).
3.  **Structuration (Transform) :** Nettoyage et chargement dans un Data Warehouse SQL (AWS RDS PostgreSQL).
4.  **Visualisation :** Affichage des recommandations sur des cartes interactives.

## Architecture
*(Insérer ici une capture d'écran de ton schéma si tu en as une, sinon supprimer cette ligne)*
> **Pipeline :** API/Scraping ➔ Python ETL ➔ AWS S3 (CSV) ➔ AWS RDS (SQL) ➔ Dashboard Plotly

## 🚀 Installation et Exécution

1.  **Cloner le dépôt:**
    ```bash
    git clone [https://github.com/TON_USER/kayak-project.git](https://github.com/athanormark/KAYAK-_-BLOC-1_JEDHA_FORMATION)
    ```

2.  **Installer les dépendances:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurer les Variables d'Environnement:**
    Créez un fichier `.env` à la racine du projet et ajoutez-y vos identifiants (ce fichier ne doit jamais être envoyé sur GitHub !) :
    ```ini
    OPENWEATHER_API_KEY=your_key
    AWS_ACCESS_KEY_ID=your_aws_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret
    AWS_BUCKET_NAME=your_bucket_name
    DB_HOST=your_db_host
    DB_USER=postgres
    DB_PASSWORD=your_db_password
    DB_NAME=postgres
    DB_PORT=5432
    ```

4.  **Lancer le Pipeline:**

* 01_Cities_list.ipynb : Récupération des coordonnées GPS des villes cibles.
* 02_Meteo_call.ipynb : Appel API pour obtenir les prévisions météo sur 7 jours.
* 03_Booking_Scraping.ipynb : Scraping des données hôtelières (méthode robuste requests avec logique de réessai).
* 04_Upload_S3.ipynb : Envoi des fichiers CSV bruts vers le Data Lake AWS S3.
* 05_SQL_RDS.ipynb : Nettoyage et chargement des données dans la base PostgreSQL AWS RDS.
* 06_Plotly_Viz.ipynb : Génération des cartes de recommandation interactives.

## 📊 Visualizations
The final output includes two interactive maps:
1.  **Top 5 Weather Destinations**
2.  **Top 20 Hotels in recommended areas**

## 👤 Author
Athanor SAVOUILLAN