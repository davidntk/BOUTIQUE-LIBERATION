# BOUTIQUE LIBERATION

Application web de gestion d'une boutique de chaussures, développée avec **Python, Flask, SQLite, HTML, CSS et JavaScript**. Le périmètre suit le Product Backlog du dépôt.

## Fonctionnalités disponibles
- Catalogue public et recherche de chaussures par nom/catégorie/couleur.
- Catégories Homme, Femme, Sport et Cuir.
- Espace administrateur protégé par une connexion.
- Ajout et suppression de produits avec prix d'achat et de vente.
- Gestion du stock par pointure.
- Enregistrement des entrées et sorties et historique des mouvements.
- Enregistrement des ventes avec contrôle de disponibilité et décrémentation automatique du stock.
- Modes de paiement : espèces, Airtel Money, Orange Money, M-Pesa et paiement à la livraison.
- Tableau de bord, alertes lorsque le stock d'une pointure est inférieur ou égal à 2 et facture imprimable.

## Installation Windows
1. Installer Python 3.
2. Ouvrir le dossier du projet dans VS Code.
3. Dans le terminal :
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```
4. Ouvrir **http://127.0.0.1:5001** dans le navigateur.

La base SQLite `boutique.db` et les données de démonstration sont créées automatiquement au premier lancement.

## Connexion de démonstration
- Identifiant : `admin`
- Mot de passe : `admin123`

**Sécurité :** ces identifiants sont uniquement destinés aux tests locaux. Avant tout déploiement, remplacer le mot de passe de démonstration, définir une variable d'environnement `SECRET_KEY` forte et mettre en place une gestion sécurisée des mots de passe. Ne pas exposer le serveur de développement Flask sur Internet.

## Structure
```
BOUTIQUE-LIBERATION/
├── app.py
├── requirements.txt
├── PRODUCT_BACKLOG.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── admin.html
│   ├── products.html
│   ├── stock.html
│   ├── sales.html
│   └── invoice.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Limites de cette version
Cette version est une base fonctionnelle de projet académique. L'authentification utilise encore un mot de passe de démonstration en clair : elle doit être renforcée avant une utilisation réelle. L'image produit est renseignée par URL (pas encore par téléversement de fichier). Le calcul du bénéfice, la gestion complète des utilisateurs et la gestion des fournisseurs restent à développer.
## Base de données locale SQLite

L'application est reliée à une base de données SQLite locale. Au premier lancement, `app.py` lit `database/schema.sql`, crée les tables et ajoute les données de démonstration si la base est vide.

- Fichier de données : `boutique.db` à la racine du projet.
- Schéma SQL : `database/schema.sql`.
- Les ventes, produits, pointures et mouvements de stock sont enregistrés dans ce fichier sur votre ordinateur.
- Le fichier `boutique.db` est ignoré par Git : les données privées ne sont pas envoyées sur GitHub.

### Démarrer sur Windows

Dans PowerShell, depuis le dossier du projet :

```powershell
py -m venv venv
.\\venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Puis ouvrir `http://127.0.0.1:5001`.

### Sauvegarder la base

Arrêter l'application, puis copier le fichier `boutique.db` dans un dossier de sauvegarde. Ne supprimez pas ce fichier si vous souhaitez conserver vos ventes et votre stock.

Pour choisir un autre emplacement, définir la variable d'environnement `DATABASE_PATH` avant de lancer `python app.py`.
