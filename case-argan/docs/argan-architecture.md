# Argan Retail — note d'architecture

## 0. Hypothèses
- Coût d'arrêt calculé sur la marge (22 %), pas sur le chiffre d'affaires.
- Jours d'ingénierie pour A : [votre hypothèse].
- Support matériel compté dès l'année 1 (12 % du prix).

## 1. Chiffres de base
- Ratio de pointe = 19 000 / 2 400 = **7,92**. Utilisé en C pour dimensionner (3 × 7,92 ≈ 24 serveurs) et pour calculer le seuil.
- Marge par commande = 480 × 22 % = 105,6 MAD ; part perdue = 38 %.
- Arrêt du site, jour moyen : 133,3 cmd/h × 0,38 × 105,6 ≈ **5 350 MAD/h**.
- Arrêt du site, jour de pointe : 1 055,6 cmd/h × 0,38 × 105,6 ≈ **42 360 MAD/h**.
- 99,9 % → 43,2 min/mois ; 99,99 % → 4,3 min/mois. L'écart de 0,648 h vaut ≈ 3 470 MAD/mois en moyenne et ≈ 27 450 MAD/mois en pointe.
- **Conclusion :** un objectif unique sur l'année n'a pas de sens ; viser plus strict pendant les 3 semaines promotionnelles.

## 2. Décision A — cœur du campus
Tableau des paires de fibres (A1 : 36, A2 : ≈ 27, A3 : 4) face à 8 disponibles.
Un paragraphe par option (faisable ? coût ?).
Ports : cœurs à 25 %, distributions de W à 22/24 (marge nulle).
Coût A3 : 554 000 MAD de matériel. A4 : 830 000 MAD, soit 276 000 MAD de plus ≈ 8,1 commutateurs d'accès.
**Recommandation :** A3. Fait déterminant : 8 paires libres.
Test « H perdu » : W perd son cœur, acceptable si la plateforme n'est pas dans H et si W a son propre WAN.
Seuil d'inversion : tranchée < 460 MAD/m, ou W grandit de plus de 8 accès.

## 3. Décision B — segmentation et carte
Coûts uniques : B1 = 32 400, B2 = 359 600, B3 = 477 200 MAD.
B4 sur 3 ans : 189 200 MAD ; net de l'audit (360 000) : −170 800 MAD.
B4 + B2 : 188 800 MAD net, contre 477 200 pour B3 → écart de **288 400 MAD en faveur de B4 + B2**.
Piège MAC-auth : une adresse MAC se lit sur l'étiquette, c'est de l'identification et non de l'authentification, donc le NAC n'apporte presque rien pour les scanners.
Paragraphe « ce que je ne protège pas » : l'identité individuelle des scanners, acceptable parce que leur portée est limitée au datacentre.

## 4. Décision C — plateforme
Dimensionnement : 24 serveurs, utilisation moyenne 12,5 %.
Tableau 3 ans / 5 ans : C1 = 4 016 560 / 4 704 400 ; C2 = 3 192 800 / 3 744 800 ; C3 = 1 877 360 / 2 914 000.
Seuil d'inversion C2/C3 : ratio ≈ 4,25 (3 ans) et ≈ 6,0 (5 ans). Argan est à 7,92.
Ce que C3 apporte : une dépendance au lien (deux opérateurs, SLA chiffré) et une facture qui croît (dominante au-delà d'environ 15 %/an sur 5 ans).
**Recommandation :** C3. Déclencheur : ratio < 6, croissance de la location > 15 %/an, lien sous son SLA.

## 5. Interdépendances
- B change C : sans données de carte, l'isolation stricte des locataires perd sa raison d'être, donc C2 suffirait à la place de C1 (≈ 824 000 MAD de moins sur 3 ans).
- C change A : plateforme en colocation = W indépendant de H pour les commandes, ce qui rend A3 acceptable.

## 6. Ce que je décide de ne pas acheter
Le NAC 802.1X (96 000 MAD). Ce qui me ferait changer d'avis : un audit exigeant l'authentification des postes.

## 7. Le script de contrôle
Défaut : il vérifiait l'unicité des VLAN mais annonçait l'isolation.
Famille : le contrôle d'un proxy au lieu de la propriété (vert par construction).
Résultats de mes trois essais de casse : [à compléter].