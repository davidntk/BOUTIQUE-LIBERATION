# BOUTIQUE LIBERATION

Application web de gestion d'une boutique de chaussures, organisée avec Flask et une interface HTML/CSS/JavaScript.

## Démarrage local

```bash
python -m venv .venv
# Windows :
.venv\Scripts\activate
# macOS / Linux :
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Ouvrir ensuite http://127.0.0.1:5000.

## Fonctionnalités de l'interface

- Tableau de bord : ventes du jour, chiffre d'affaires, bénéfice estimé et total en stock.
- Alertes de stock faible et produits épuisés.
- Catalogue client avec recherche, filtres Homme/Femme/Sport/Cuir, prix, couleur, photo et disponibilité.
- Gestion des produits, catégories, pointures et quantités.
- Entrées et sorties de stock par pointure.
- Panier, choix de pointure et formulaire de commande.
- Choix de paiement affichés : Airtel Money, Orange Money, M-Pesa et paiement à la livraison.
- Gestion des fournisseurs, rapports et export CSV.

## Données et limites actuelles

Les données métier sont encore conservées dans le navigateur via `localStorage`. Elles ne sont donc pas partagées entre appareils ou utilisateurs. Les données initiales sont des exemples de démonstration.

Les moyens de paiement mobiles sont uniquement des choix affichés : aucune transaction réelle n'est déclenchée. L'authentification, les rôles utilisateurs, une base de données serveur, les factures et l'intégration réelle des prestataires de paiement restent à développer avant une mise en production.

L'application Flask actuelle sert l'interface et expose `/health` pour vérifier que le serveur répond.
