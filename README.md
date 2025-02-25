# 🚆 Suivi en temps réel des retards des TER SNCF avec Kafka
*Ce projet est un exercice personnel et n'est pas affilié à la SNCF.*

## 🔎 Contexte
On me dit souvent que la SNCF a tendance à être en retard un peu trop souvent. Est-ce vrai, ou est-ce simplement un effet de saillance qui nous pousse à remarquer davantage les retards que les trains à l’heure ? (Spoiler Alert, c'est bel et bien un effet de saillance !)

Dans le doute, je me suis dit que j'allais faire ce que je fais de mieux...Et m'amuser avec des données. 

On va setup un process qui permettrait de vérifier notre hypothèse, en prenant des données en temps réel de chez la SNCF ! 

Si on fait tourner ce projet assez longtemps sur une machine assez performante (ou si on prend simplement en compte les recommendations que j'ai posées en fin de projet pour une version plus optimisée), on peut répondre à cette question avec assez de détail, mais les résultats que j'ai obtenus étaient déjà intéressants.

J'ai pris le parti pris de faire un petit dashboard en "temps réel" (mis à jour toutes les 2 minutes en raison des limites du GTFS-RT TU), histoire de pouvoir observer les évolutions en temps réel.

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

Ce projet n’a pas vocation à être utilisé en production, mais sert à démontrer comment Kafka peut être utilisé pour du traitement de flux en temps réel, et accessoirement, c'est un petit exercice qui m'a permis de me familiariser avec Kafka en dehors de lectures théoriques...!

<br>

## 📒 Et après ?

- Actuellement, on récupère tous les retards, mais on pourrait affiner en **filtrant par gare, par exemple.**
- Ajouter un **stockage persistant** (comme **PostgreSQL** ou **DuckDB**) pour historiser les retards.
- Pourquoi pas un **modèle de prédiction** des retards à partir des historiques ?

<br>

## 🗃️ Data Source 
Réseau national TER SNCF : https://transport.data.gouv.fr/datasets/horaires-des-lignes-ter-sncf
