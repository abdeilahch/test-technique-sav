# Ticket API

API REST de gestion de tickets développée avec FastAPI, SQLAlchemy et Pydantic.  
Elle permet la création, la mise à jour, la consultation et la fermeture de tickets.

## Stack
- Python 3.10+
- FastAPI
- SQLAlchemy (SQLite)
- Pydantic v2
- Pytest
- Docker

## Installation et démarrage
# Installation
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configuration
Créer un fichier `.env` à la racine du projet avec les variables suivantes :
APP_NAME=Ticket API
APP_DESCRIPTION=API de gestion de tickets
DEBUG=True
HOST=0.0.0.0 # Adresse d’écoute du serveur
PORT=8000 # Port d’exposition de l’API
DATABASE_URL=sqlite+pysqlite:///:memory:

# Lancement
uvicorn app.main:app --reload
# Lancement Docker
docker build -t ticket-api .
docker run -d -p 8000:8000 --name ticket-api ticket-api

## Documentation Swagger
http://127.0.0.1:8000/docs

## Structure
├── app/                # Code principal de l’application
│   ├── api/            # Routes FastAPI
│   ├── core/           # Middleware, exceptions, logging
│   ├── crud/           # Logique métier et accès base de données
│   ├── db/             # Configuration et initialisation de la base
│   ├── models/         # Modèles SQLAlchemy
│   ├── schemas/        # Schémas Pydantic
│   ├── utils/          # Fonctions utilitaires
│   ├── config.py       # Paramètres et lecture du fichier .env
│   └── main.py         # Point d’entrée FastAPI
├── tests/              # Tests unitaires Pytest
├── Dockerfile          # Image Docker de l’application
├── requirements.txt    # Dépendances Python
├── .env                # Variables d’environnement
└── README.md           # Documentation du projet


## Endpoints
Méthode | URL | Description
-------- | --- | -----------
POST | /tickets/ | Créer un ticket
GET | /tickets/ | Lister les tickets (pagination)
GET | /tickets/{id} | Récupérer un ticket
PUT | /tickets/{id} | Modifier un ticket
PATCH | /tickets/{id}/close | Fermer un ticket

## Exemple d’utilisation

### Création d’un ticket
```bash
curl -X POST http://127.0.0.1:8000/tickets/      -H "Content-Type: application/json"      -d '{"title": "Incident réseau", "description": "Coupure fibre sur le site A"}'
```
**Réponse :**
```json
{
  "id": 1,
  "title": "Incident réseau",
  "description": "Coupure fibre sur le site A",
  "status": "open",
  "created_at": "2025-10-29T14:32:00Z"
}
```

###  Récupération d’un ticket
```bash
curl http://127.0.0.1:8000/tickets/1
```
**Réponse :**
```json
{
  "id": 1,
  "title": "Incident réseau",
  "description": "Coupure fibre sur le site A",
  "status": "open",
  "created_at": "2025-10-29T14:32:00Z"
}
```

###  Mise à jour d’un ticket
```bash
curl -X PUT http://127.0.0.1:8000/tickets/1      -H "Content-Type: application/json"      -d '{"title": "Incident fibre", "description": "Problème sur le routeur"}'
```
**Réponse :**
```json
{
  "id": 1,
  "title": "Incident fibre",
  "description": "Problème sur le routeur",
  "status": "open",
  "created_at": "2025-10-29T14:32:00Z"
}
```

###  Fermeture d’un ticket
```bash
curl -X PATCH http://127.0.0.1:8000/tickets/1/close
```
**Réponse :**
```json
{
  "id": 1,
  "title": "Incident fibre",
  "description": "Problème sur le routeur",
  "status": "closed",
  "created_at": "2025-10-29T14:32:00Z"
}
```

###  Récupération paginée des tickets
```bash
curl http://127.0.0.1:8000/tickets/?page=1&per_page=10
```
**Réponse :**
```json
{
  "total": 1,
  "total_pages": 1,
  "current_page": 1,
  "per_page": 10,
  "tickets": [
    {
      "id": 1,
      "title": "Incident fibre",
      "description": "Problème sur le routeur",
      "status": "closed",
      "created_at": "2025-10-29T14:32:00Z"
    }
  ]
}
```

## Fonctionnalités
- Création, lecture, mise à jour, fermeture de tickets  
- Statut : open, stalled, closed  
- Pagination avec paramètres page et per_page (≤500)  
- Validation et échappement XSS (html.escape)  
- Middleware de logs avec mesure du temps de traitement (X-Process-Time)  
- Documentation Swagger générée automatiquement  

## Base de données
- SQLite en mémoire via SQLAlchemy  
- Schéma : Ticket(id, title, description, status, created_at)  
- COUNT() utilisé pour la pagination
  - En production : remplacer par une estimation ou un cache (PostgreSQL/Redis)  
- Index en production :  
  - CREATE INDEX idx_tickets_status ON tickets(status);
  - CREATE INDEX idx_tickets_created_at ON tickets(created_at);

## Tests
pytest -v
-Tests Couverture :
- CRUD complet  
- Pagination  
- Validation et XSS  
- Ticket inexistant (404)  
- Temps de réponse < 200 ms (middleware)
