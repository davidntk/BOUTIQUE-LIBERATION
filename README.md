# BOUTIQUE LIBERATION

Application web de boutique de chaussures construite avec Python, Flask, SQLite, HTML, CSS et JavaScript.

## Structure

```
BOUTIQUE-LIBERATION/
├── app.py
├── requirements.txt
├── PRODUCT_BACKLOG.md
├── templates/
│   ├── index.html
│   └── admin.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Installation sous Windows

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Ouvrir ensuite http://127.0.0.1:5001

## Pages

- / : accueil et catalogue avec recherche et filtres.
- /admin : tableau de bord, ajout et suppression de produits.

La base SQLite et des produits de démonstration sont créés automatiquement au premier lancement.

## État du projet

Cette première version fournit la structure web et une gestion initiale du catalogue et des produits. L'authentification administrateur, la gestion détaillée des pointures et mouvements de stock, les ventes, les factures et l'intégration réelle des paiements restent à développer. Le bouton de sélection du catalogue utilise actuellement le stockage local du navigateur et ne réalise aucun paiement.
