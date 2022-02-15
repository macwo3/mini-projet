
API mini projet

Cette API permet de gérer une table etudiants créée dans la base de données.

Commencer

Installation des dépendances
Python 3.9.7
pip 20.3.4 à partir de /usr/lib/python3/dist-packages/pip (python 3.9)
Si vous n’avez pas python installé, merci de suivre cet URL pour l’installer python docs

Environnement virtuel
Vous devez installer le package dotenv en utilisant la commande pip install python-dotenv

Dépendances PIP
Exécuter la commande ci dessous pour installer les dépendences

pip install -r requirements.txt
or
pip3 install -r requirements.txt
Cela installera tous les packages requis que nous avons sélectionnés dans le fichier.requirements.txt

Dépendances clés
Flask est un framework de microservices backend léger. Flask est nécessaire pour traiter les demandes et les réponses.

SQLAlchemy est la boîte à outils SQL Python et ORM que nous utiliserons pour gérer la base de données sqlite légère. Vous travaillerez principalement dans app.py et pourrez vous référer à models.py.

Flask-CORS est l’extension que nous utiliserons pour gérer les demandes d’origine croisée de notre serveur frontal.

Configuration de la base de données
Avec Postgres en cours d’exécution, restaurez une base de données à l’aide du fichier projet.sql fourni. À partir du dossier principal dans le terminal, exécutez :

psql projet < projet.sql
Exécution du serveur
À partir de l’annuaire, assurez-vous d’abord que vous travaillez à l’aide de l’environnement virtuel que vous avez créé.projet

Pour exécuter le serveur sous Linux ou Mac, exécutez :

export FLASK_APP=api2
export FLASK_ENV=development
flask run
Pour exécuter le serveur sous Windows, exécutez :

set FLASK_APP=api2
set FLASK_ENV=development
flask run

RÉFÉRENCE API
Getting starter

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://localhost:5000; which is set as a proxy in frontend configuration.

Error Handling
Errors are retourned as JSON objects in the following format: { "success":False "error": 400 "message":"Bad request" }

The API will return four error types when requests fail: . 400: Bad request . 500: Internal server error . 422: Unprocessable . 404: Not found

Endpoints
. ## GET/livres

GENERAL: cet endpoint permet de récupérer la liste des livres 

{
    "livres": [
        {
            "ISBN": 4334,
            "auteur": "auteur1",
            "date_publication": "Sat, 01 Jan 2022 00:00:00 GMT",
            "editeur": "editeur1",
            "id": 1,
            "titre": "fiction1"
        },
        {
            "ISBN": 4335,
            "auteur": "auteur2",
            "date_publication": "Fri, 21 Jan 2022 00:00:00 GMT",
            "editeur": "editeur2",
            "id": 2,
            "titre": "fiction2"
        },
        {
            "ISBN": 4435,
            "auteur": "auteur2",
            "date_publication": "Fri, 21 Jan 2022 00:00:00 GMT",
            "editeur": "editeur2",
            "id": 3,
            "titre": "aventure1"
        },
        {
            "ISBN": 4455,
            "auteur": "auteur2",
            "date_publication": "Mon, 21 Mar 2022 00:00:00 GMT",
            "editeur": "editeur2",
            "id": 4,
            "titre": "aventure2"
        },
        {
            "ISBN": 4415,
            "auteur": "auteur3",
            "date_publication": "Sun, 21 Mar 2021 00:00:00 GMT",
            "editeur": "editeur3",
            "id": 5,
            "titre": "aventure3"
        },
        {
            "ISBN": 1415,
            "auteur": "auteur4",
            "date_publication": "Sat, 21 Mar 2020 00:00:00 GMT",
            "editeur": "editeur3",
            "id": 6,
            "titre": "horreur1"
        }
    ],
    "success": true,
    "total livres": 6
}

    
SAMPLE: curl -i http://localhost:5000/livres

. ## GET/categories

GENERAL: cet endpoint permet de récupérer la liste des categories 

{
    "categories": [
        {
            "id": 1,
            "libelle_categorie": "fiction"
        },
        {
            "id": 2,
            "libelle_categorie": "aventure"
        },
        {
            "id": 3,
            "libelle_categorie": "horreur"
        }
    ],
    "success": true,
    "total categories": 3
}


. ## GET/livres (id)

GENERAL: Cet endpoint permet de chercher un livre par son id
Les resulats de cette requete se présentent comme suit:

{
    "livre": {
        "ISBN": 4335,
        "auteur": "auteur2",
        "date_publication": "Fri, 21 Jan 2022 00:00:00 GMT",
        "editeur": "editeur2",
        "id": 2,
        "titre": "fiction2"
    },
    "selected_id": 2,
    "success": true
}


. ## GET/categories (id)

GENERAL: Cet endpoint permet de chercher une categorie par son id
Les resulats de cette requete se présentent comme suit:

{
    "categorie": {
        "id": 2,
        "libelle_categorie": "aventure"
    },
    "selected_id": 2,
    "success": true
}

. ## DELETE/livres (id)

GENERAL: Cet endpoint permet de supprimer un livre
Les resulats de cette requete se présentent comme suit:

{
    "deletedted_id": 1,
    "livre": {
        "ISBN": 4334,
        "auteur": "auteur1",
        "date_publication": "Sat, 01 Jan 2022 00:00:00 GMT",
        "editeur": "editeur1",
        "id": 1,
        "titre": "fiction1"
    },
    "success": true
}

. ## DELETE/categories (id)

GENERAL: Cet endpoint permet de supprimer une categorie par son id

{
    "categorie": {
        "id": 1,
        "libelle_categorie": "fiction"
    },
    "selected_id": 1,
    "success": true
}
 

. ##PATCH/livres(id)

  GENERAL:
   Cet endpoint permet de modifier un livre et retourne le livre modifié

   {
    "livre": {
        "ISBN": 123,
        "auteur": "Ferdinand",
        "date_publication": "Mon, 02 Mar 2020 00:00:00 GMT",
        "editeur": "david",
        "id": 3,
        "titre": "une vie de boy"
    },
    "success": true,
    "updated_id": 3
}

. ##PATCH/categories(id)

  GENERAL:
   Cet endpoint permet de modifier une categorie et retourne la categorie modifiée*


   {
    "livre": {
        "id": 3,
        "libelle_categorie": "horreur"
    },
    "success": true,
    "updated_id": 3
}

