# DESIGN — Boutique Libération

## Aperçu
Maquette front-end responsive de la boutique en ligne Boutique Libération, pensée pour Lubumbashi (RDC). Ouvrir `index.html` dans un navigateur pour parcourir le design.

## Identité visuelle
- **Rose** : douceur et élégance (`#E9A4B5`, fond rose pâle `#F8E7EC`)
- **Jaune** : accent lumineux (`#F6CF54`)
- **Noir** : typographie et contraste (`#171417`)
- **Blanc / ivoire** : espace et lisibilité (`#FFFDFB`)
- **Rouge** : actions et accents (`#D73543`)

## Catalogue présenté
### Hommes
Polos, Chemises, Lacoste, Pantalons, Tissus, Jeans tissus, Chaussures hommes, Cuirs.

### Femmes
Robes, Pagnes, Jupes, Polos femmes, Bodys, Chaussures femmes, Baskets femmes, New Balance.

## Éléments de la maquette
- En-tête avec identité, recherche et panier.
- Bannière d'accueil et accès aux univers.
- Filtres par rayon et recherche instantanée.
- Cartes produits avec photos, catégories, prix indicatifs en USD et favoris visuels.
- Panier interactif avec quantités et total estimé.
- Mise en page adaptée au mobile et à l'ordinateur.

## Conservation de l'ancien cahier des charges
Le contenu de l'ancien fichier racine `DESIGN` a été conservé intégralement ci-dessous lors de sa transformation en dossier `DESIGN/` :

> 8. Design - Boutique Liberation - Par Ingenieur Ova, Designer
>
> A. Ecran d'accueil / Catalogue Client
> - Top Bar : Logo a gauche, Barre de recherche, Panier avec badge rouge
> - Filtres : Tous, Homme, Femme, Sport, Cuir
> - Grille Produits : Photo, Nom, Couleur, Prix en $, Badge Plus que 2 ou Epuise, Bouton Ajouter avec Pointure
>
> B. Panier et Commande
> - Tableau : Modele, Pointure, Prix, Bouton Retirer
> - Paiement : Nom, Numero de telephone, Airtel Money, Orange Money, M-Pesa, Paiement a la livraison
> - Bouton : Valider le paiement
>
> C. Espace Administrateur - Dashboard
> - KPI : Ventes du jour, Chiffre d'affaires, Benefice net, Total en stock
> - Alerte rouge si stock inferieur ou egal a 2
>
> D. Gestion des Produits et Stocks
> - Formulaire : Nom, Categorie, Prix d'achat, Prix de vente, Pointure, Quantite, Photo
> - Tableau par pointure : Exemple T40 : 3, T41 : 0 barre si epuse

## Notes avant développement
- Les prix sont des exemples de présentation, à remplacer par les vrais prix et devises de vente.
- Les photos sont chargées depuis Unsplash via Internet et servent d'illustrations de maquette.
- Les boutons de panier sont interactifs côté navigateur. Le paiement, les comptes clients, les stocks, les pointures réelles et l'administration ne sont pas connectés : ils seront développés ensuite.
- Les moyens de paiement à intégrer selon le cahier des charges : Airtel Money, Orange Money, M-Pesa et paiement à la livraison.
