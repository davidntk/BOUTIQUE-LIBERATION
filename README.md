# BOUTIQUE LIBERATION

Application web de boutique de chaussures construite avec Python, Flask, SQLite, HTML, CSS et JavaScript.

## Structure

```
BOUTIQUE-LIBERATION/
├── app.py
├── requirements.txt
├── PRODUCT_BACKLOG.md
├── Dockerfile
├── compose.yaml
├── .env.example
├── run-local.bat
├── run-local.sh
├── templates/
│   ├── index.html
│   └── admin.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Démarrage local sous Windows (sans Docker)

1. Installer Python 3.
2. Double-cliquer sur `run-local.bat`.
3. Attendre l'installation des dépendances et le démarrage du serveur.
4. Ouvrir les adresses suivantes :

- Boutique : http://127.0.0.1:5001
- Administration : http://127.0.0.1:5001/admin
- Vérification : http://127.0.0.1:5001/health

Le script crée automatiquement un environnement virtuel et un dossier `data` pour la base SQLite.

Sous Linux/macOS, lancer `chmod +x run-local.sh`, puis `./run-local.sh`.

## Déploiement local avec Docker

Prérequis : Docker Desktop (Windows/macOS) ou Docker Engine avec le plugin Compose (Linux).

1. Copier `.env.example` vers `.env`.
2. Remplacer `SECRET_KEY` dans `.env` par une longue valeur aléatoire.
3. Dans le dossier du projet, exécuter :

```bash
docker compose up --build -d
```

Puis ouvrir http://127.0.0.1:5001.

Commandes utiles :

```bash
docker compose ps
docker compose logs -f
docker compose down
```

Les données SQLite sont conservées dans le volume Docker `boutique_data`, même après `docker compose down`. Pour supprimer aussi les données, utiliser explicitement `docker compose down -v` (opération destructive).

Pour changer le port local, modifier `APP_PORT` dans `.env` (par exemple `APP_PORT=8080`), puis relancer Compose.

## Accès depuis un autre appareil du même réseau

Le serveur écoute sur toutes les interfaces réseau. Depuis un autre appareil connecté au même Wi-Fi, ouvrir :

`http://ADRESSE-IP-LOCALE-DU-PC:5001`

Remplacer l'adresse par l'IPv4 du PC qui héberge l'application. Autoriser Python ou Docker dans le pare-feu Windows uniquement sur le réseau privé si nécessaire. Ne pas exposer directement cette application sur Internet : elle ne dispose pas encore d'une authentification administrateur.

## Pages et état fonctionnel

- `/` : accueil et catalogue avec recherche et filtres.
- `/admin` : tableau de bord, ajout et suppression de produits.
- `/health` : vérification simple de l'application et de SQLite.

La base SQLite et les produits de démonstration sont créés automatiquement au premier lancement si la base est vide.

Cette première version fournit la structure web et une gestion initiale du catalogue et des produits. L'authentification administrateur, la gestion détaillée des pointures et mouvements de stock, les ventes, les factures et l'intégration réelle des paiements restent à développer. Le bouton de sélection du catalogue utilise actuellement le stockage local du navigateur et ne réalise aucun paiement.
