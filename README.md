# 🚆 Suivi en temps réel de la ponctualité des TER SNCF avec Kafka
*Ce projet est un exercice personnel et n'est pas affilié à la SNCF.*

## 🔎 Contexte
La ponctualité des trains est souvent perçue de manière subjective : avons-nous tendance à davantage remarquer les retards que les trains à l’heure, ou ces retards sont-ils réellement fréquents ?

Pour explorer cette question, j’ai voulu analyser des données publiques en temps réel de la SNCF. J’ai ainsi mis en place un process permettant d’observer et de visualiser l’évolution des horaires de trains en direct.

Pour ce projet, j’ai conçu un dashboard qui récupère des données en streaming, mises à jour toutes les 2 minutes en raison des limites du GTFS-RT TU. J’y propose également quelques pistes d’optimisation pour améliorer le suivi des données.

Les premières observations montrent que les retards sont peu fréquents, ce qui pourrait indiquer que nos biais cognitifs joueraient un rôle important dans notre perception de la ponctualité des TER.

<br>

## 🚀 Comment ça marche ?

### 1️⃣ Lancer l’environnement Kafka

Avant tout, il faut démarrer **Kafka** et **Zookeeper.**\
Tout est déjà configuré dans **`docker-compose.yml`**, donc un simple :

```bash
docker-compose up -d
```

... et c’est parti ! Kafka tourne en tâche de fond.


### 2️⃣ Démarrer le Producteur

Le **producer** va envoyer des messages Kafka contenant les données de retard des trains en temps réel.

```bash
python producer.py
```

Ce script va récupérer les mises à jour **GTFS-RT** et les envoyer dans le topic **`sncf-realtime`**.


### 3️⃣ Démarrer le Consumer + Dashboard

Une fois les messages envoyés, il faut un **consumer** pour les traiter et les afficher.\
Lance-le avec :

```bash
python realtime_train_delays.py
```

Celui-ci :

- Agrège les données en **temps réel**
- Met à jour un **dashboard en live** via **Plotly Dash**
- Affiche un **histogramme des retards actuels**

Accède ensuite à l’interface via ton navigateur :

```
http://127.0.0.1:8050
```

*(Le lien s'affichera dans le Terminal au lancement du script.)*

<br>

## 📊 Données visualisées

✅ **Retards en minutes**, classés par intervalles (`0`, `1-5`, `6-10`, etc.)\
✅ **Mise à jour toutes les 2 minutes** (fréquence des messages Kafka)\
✅ **Histogramme dynamique** qui évolue en fonction des données entrantes

<br>

## 🏢 Tech Stack

⚫ **Kafka** pour la gestion des flux de données\
⚫ **Docker** pour l’orchestration\
⚫ **Python** (`kafka-python`, `dash`, `plotly`, `pandas`, etc.)\
⚫ **GTFS-RT** pour les données de transport en temps réel

<br>

## 🎯 Objectif ?

Ce projet n’a pas vocation à être utilisé en production, mais illustre comment Kafka peut servir au traitement de flux en temps réel. C'était aussi une bonne occasion de me familiariser avec Kafka au-delà des lectures théoriques...!

<br>

## 📒 Et après ?

- Actuellement, on récupère tous les retards, mais on pourrait affiner en **filtrant par gare, par exemple.**
- Ajouter un **stockage persistant** (comme **PostgreSQL** ou **DuckDB**) pour historiser les retards.
- Pourquoi pas un **modèle de prédiction** des retards à partir des historiques ?

<br>

## 🗃️ Data Source 
Réseau national TER SNCF : https://transport.data.gouv.fr/datasets/horaires-des-lignes-ter-sncf
