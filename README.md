# 🚆 Suivi en temps réel des retards SNCF avec Kafka

## 🚀 Comment ça marche ?

### 1️⃣ Lancer l’environnement Kafka

Avant tout, il faut démarrer **Kafka** et **Zookeeper**.\
Tout est déjà configuré dans **`docker-compose.yml`**, donc un simple :

```bash
docker-compose up -d
```

... et c’est parti ! Kafka tourne en tâche de fond.

---

### 2️⃣ Démarrer le Producteur

Le **producer** va envoyer des messages Kafka contenant les données de retard des trains en temps réel.

```bash
python producer.py
```

Ce script va récupérer les mises à jour **GTFS-RT** et les envoyer dans le topic **`sncf-realtime`**.

---

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

---
*(Le lien s'affichera dans le Terminal au lancement du script.)*


## 📊 Données visualisées

✅ **Retards en minutes**, classés par intervalles (`0`, `1-5`, `6-10`, etc.)\
✅ **Mise à jour toutes les 2 minutes** (fréquence des messages Kafka)\
✅ **Histogramme dynamique** qui évolue en fonction des données entrantes

---

## 🏢 Tech Stack

⚫ **Kafka** pour la gestion des flux de données\
⚫ **Docker** pour l’orchestration\
⚫ **Python** (`kafka-python`, `dash`, `plotly`, `pandas`, etc.)\
⚫ **GTFS-RT** pour les données de transport en temps réel

---

🎯 Objectif ?



Ce projet n’a pas vocation à être utilisé en production, mais sert à démontrer comment Kafka peut être utilisé pour du traitement de flux en temps réel, et accessoirement, c'est un petit exercice qui m'a permis de me familiariser avec Kafka en dehors de lectures théoriques...!

---

## 📒 Et après ?

- Actuellement, on récupère tous les retards, mais on pourrait affiner en **filtrant par ligne, gare ou destination**.
- Ajouter un **stockage persistant** (comme **PostgreSQL** ou **DuckDB**) pour historiser les retards.
- Pourquoi pas un **modèle de prédiction** des retards à partir des historiques ?

