# BOUTIQUE LIBERATION

Application web de gestion d'une boutique de chaussures, réalisée à partir du Product Backlog.

## Démarrage
Ouvrir `index.html` dans un navigateur moderne. Aucune installation n'est requise.

## Fonctionnalités
- Tableau de bord : ventes, chiffre d'affaires, quantité en stock et alertes.
- Catalogue et gestion des produits : catégories, prix d'achat/vente, pointures et quantités.
- Entrées et sorties de stock par pointure.
- Boutique client avec recherche, panier et choix de pointure.
- Enregistrement d'une vente avec déduction automatique du stock.
- Modes de paiement affichés : Airtel Money, Orange Money, M-Pesa et paiement à la livraison.
- Gestion des fournisseurs.
- Rapports, estimation de marge et export CSV.

## Stockage et limites
Les données sont conservées localement dans le navigateur via `localStorage`. Elles ne sont pas partagées entre appareils. Les données initiales sont des exemples de démonstration.
Les moyens de paiement mobiles sont uniquement proposés comme choix de paiement : aucune transaction réelle n'est exécutée. Pour une mise en production, il faudra ajouter une API/backend sécurisé, une base de données, une authentification avec rôles et l'intégration officielle des prestataires de paiement.
