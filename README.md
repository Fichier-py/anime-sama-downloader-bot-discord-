# 📺 Anime Downloader Discord Bot

Le Anime Downloader Discord Bot est un projet Python conçu pour automatiser le processus de recherche, téléchargement et distribution d’épisodes d’anime directement depuis Discord. Il combine plusieurs technologies (Discord.py, yt-dlp, Flask et ngrok) afin de créer un système complet allant de la sélection d’un contenu jusqu’à la génération de liens de téléchargement accessibles en ligne.

L’objectif du bot est de simplifier l’accès à des épisodes d’anime en automatisant plusieurs étapes techniques qui seraient normalement manuelles : récupération des liens vidéo sur des pages web, téléchargement des fichiers, hébergement local temporaire et génération de liens publics.

---

## 🧠 Principe de fonctionnement global

Le système repose sur une architecture en trois couches :

### 1. Interface utilisateur (Discord)
Le bot Discord agit comme interface principale. L’utilisateur interagit uniquement via des commandes simples. Chaque commande permet de définir un paramètre précis :
- nom de l’anime
- saison
- langue
- plage d’épisodes

Ces informations sont stockées temporairement en mémoire dans des variables globales, utilisées ensuite pour construire les requêtes vers les sources externes.

---

### 2. Extraction et téléchargement des épisodes
Une fois la commande de téléchargement lancée, le bot construit une URL vers un site de catalogue d’anime. Cette URL suit une structure précise basée sur les paramètres fournis par l’utilisateur.

Le bot envoie ensuite une requête HTTP vers cette page et analyse le contenu HTML/JS afin d’extraire les liens vidéo. L’extraction repose sur des expressions régulières ciblant deux principales sources :
- sibnet.ru
- sendvid.com

Ces liens sont ensuite passés à `yt-dlp`, un outil capable de télécharger des vidéos depuis différentes plateformes. Chaque épisode est téléchargé localement en fichier `.mp4`.

---

### 3. Serveur de fichiers + distribution
Une fois les vidéos téléchargées, elles sont stockées dans le dossier local du projet. Un serveur Flask est lancé en arrière-plan pour servir ces fichiers via HTTP.

Pour rendre ce serveur accessible depuis internet, le bot utilise ngrok. ngrok crée un tunnel sécurisé entre la machine locale et une URL publique. Cette URL est ensuite utilisée pour générer des liens de téléchargement envoyés sur Discord.

Après envoi des liens, les fichiers sont supprimés automatiquement pour éviter la saturation du disque.

---

## ⚙️ Commandes du bot

Le bot repose sur un système de commandes simples permettant de contrôler tout le processus.

---

### 🎬 !anime <nom>

Définit l’anime à télécharger.

Exemples :
- `!anime frieren`
- `!anime attack-on-titan`

Le nom doit correspondre à l’identifiant utilisé dans l’URL du site source. Les espaces sont remplacés par des tirets.

---

### 📀 !saison <numéro>

Définit la saison de l’anime.

Exemple :
- `!saison 1`
- `!saison 2`

Cette valeur est utilisée pour construire le chemin vers les épisodes.

---

### 🈯 !langue <vf/vostfr/vf1/vf2>

Définit la langue des épisodes.

Options possibles :
- vf (version française)
- vf1 / vf2 (variantes selon sources)
- vostfr (version originale sous-titrée)

---

### ⬇️ !run <début-fin>

Commande principale du bot.

Elle permet de télécharger une plage d’épisodes.

Exemples :
- `!run 1-1` → 1 épisode
- `!run 1-2` → 2 épisodes maximum

Contraintes :
- limite stricte de 2 épisodes par requête
- gestion d’erreurs si index incorrect ou lien absent

---

### 📁 !fichiers

Permet de récupérer les liens de téléchargement des fichiers MP4 générés.

Le bot :
1. scanne le dossier local
2. récupère tous les fichiers `.mp4`
3. génère une URL publique via ngrok
4. envoie les liens sur Discord

Après envoi, les fichiers sont supprimés automatiquement.

---

### ❓ !aide

Affiche un embed détaillé contenant :
- toutes les commandes
- les règles d’utilisation
- les limites du bot

---

## 🧩 Architecture technique détaillée

### 📡 Discord Bot
Basé sur `discord.ext.commands`, il gère :
- les commandes utilisateur
- la mémoire temporaire (anime, saison, langue)
- le déclenchement des tâches de téléchargement

---

### 🌐 Scraping
Le bot interroge dynamiquement une page de catalogue anime : https://anime-sama.to/catalogue/{anime}/saison{saison}/{langue}/episodes.js


Puis extrait les liens vidéo via regex.

---

### 📥 Téléchargement vidéo
yt-dlp est utilisé pour :
- récupérer les flux vidéo
- télécharger les fichiers en local
- gérer les erreurs réseau et formats

Options utilisées :
- format best
- timeout socket
- gestion automatique des extensions

---

### 🖥️ Serveur Flask
Flask expose les fichiers téléchargés via : /download/<filename>


Il fonctionne en arrière-plan grâce à un thread séparé.

---

### 🌍 ngrok
ngrok crée un tunnel public vers le serveur Flask :
- permet accès externe aux fichiers
- génère une URL unique
- utilisée pour partager les MP4 sur Discord

---

## 📁 Gestion des fichiers

Les fichiers sont :
- stockés localement
- nommés automatiquement par yt-dlp
- supprimés après distribution

⚠️ Aucun système de sauvegarde n’est présent.

---

## ⚠️ Limitations importantes

Ce système présente plusieurs limites structurelles :

### ❌ Pas de multi-utilisateur réel
Les variables globales entraînent des conflits si plusieurs personnes utilisent le bot en même temps.

### ❌ Pas de gestion de sessions
Les données d’un utilisateur peuvent être écrasées par un autre.

### ❌ Dépendance externe
Le bot dépend totalement de la structure du site cible. Si elle change, le bot casse.

### ❌ Suppression destructrice
Tous les fichiers MP4 sont supprimés sans vérification fine.

### ❌ Serveur public non sécurisé
Le serveur Flask est exposé via ngrok sans authentification.

---

## 🔐 Sécurité et améliorations recommandées

Pour rendre le projet plus robuste :

- utiliser `.env` pour les tokens
- ajouter authentification sur Flask
- isoler les fichiers par utilisateur Discord
- remplacer les variables globales par une structure de session
- ajouter une file d’attente de téléchargement
- limiter les accès au serveur public
- ajouter logs et monitoring

---

## 🚀 Objectif du projet

Ce projet est principalement éducatif. Il démontre comment combiner plusieurs technologies Python pour créer un système automatisé complet :

- interaction Discord
- scraping web
- téléchargement vidéo
- serveur web local
- exposition publique via tunnel

Il ne s’agit pas d’un outil de production, mais d’une démonstration technique de bout en bout d’un pipeline automatisé de récupération et distribution de contenu vidéo.

---

## 📌 Résumé

Ce bot transforme une simple commande Discord en un système complet capable de :
- sélectionner un anime
- récupérer ses épisodes
- télécharger les vidéos
- héberger les fichiers localement
- générer des liens de téléchargement publics

Le tout entièrement automatisé, mais avec des limites importantes en termes de sécurité et de scalabilité.
