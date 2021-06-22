# App Agence Immobilière - Estimation de prix
[![Build Status](https://travis-ci.com/SimplonAI/api-mmo.svg?token=54ssNXAp4tdWQ5mk1zsT&branch=main)](https://travis-ci.com/SimplonAI/api-mmo)

Notre application se base sur le dataset Housing California de 1990.

# Prérequis
* Python 3.9
* PostgreSQL
ou
* Docker
    * Suivre seulement l'étape Docker

# Installation
```console
git clone https://github.com/SimplonAI/api-mmo
cd api-mmo
python -m venv venv
```
Sur Windows exécutez :
```console
venv/Scripts/activate
```
ou sur Linux :
```console
source venv/bin/activate
```
Ensuite finir par :
```console
pip install -r requirements.txt
```

# Configuration
Ouvrir le fichier `exemple_config.json` et remplacer les valeurs par défaut par celle de votre environnement. Copier ensuite ce fichier dans un dossier instance et le renommer config.json.
```console
mkdir instance
cp exemple_config.json instance/config.json
```
Ensuite exécuter les commandes de configuration pour la BDD:
```console
flask db upgrade
flask insert-db
```

# Créer un utilisateur
Afin d'utiliser l'app, vous allez devoir vous connecter avec un utilisateur. Pour le créer :
```console
flask create-user
```

# Exécution
Pour lancer l'app, vous devrez taper la commande :
```console
flask run
```

# Estimer un prix médian
Afin d'estimer un prix médian grâce à notre fonction ML, vous aurez besoin de rentrer les informations demandés après avoir taper la commande :
```console
flask predict-value
```

# Docker
Si vous voulez vous éviter toutes les instructions précédentes, il est conseillé d'utiliser Docker.
## Configuration
Il faut configurer les variables environnements de Postgres dans un fichier .env à placer à la racine de l'application (renommer le fichier `.env.exemple` en `.env` suffit amplement) :
```console
cp .env.exemple .env
```
## Construire et exécuter l'image docker :
```console
docker-compose up -d
```
## Connexion au conteneur de l'appplication et création d'un utilisateur:
1. Lister les conteneur actif :
```console
docker ps
```
2. Selectionner le "CONTAINER_ID" du conteneur "api-mmo_website"

3. Connecter vous au bash du conteneur et crée l'utilisateur de l'application Flask:
```console
docker exec -it "CONTAINER_ID" flask create-user
```
4. De la même manière il sera possible d'exécuter les autres commandes flask.
