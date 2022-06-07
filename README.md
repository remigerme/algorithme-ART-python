# Simulations autour de l'algorithme ART

Ce projet a été réalisé dans le cadre de mon TIPE (projet de classes préparatoires).

On retrouve une implémentation de l'algorithme ART dans `src/resolution.py`. Tous les fichiers python du projet se trouvent dans `src/`.

## Simulations
Le coeur du projet consiste à étudier l'influence de différents paramètres de l'algorithme ART, qu'ils concernent la préparation des données de projection ou l'exécution de l'algorithme. Pour ce faire, j'ai successivement fait varié les paramètres ci-dessous, sur deux images : le "Shepp Logan phantom" (SLP), une image de test standard en tomographie, ainsi qu'une photo de mon lapin. Les images cibles sont disponibles dans `exemples/slp/` et `exemples/lapin/`, et les résultats des simulations se trouvent dans `simulations/`.

### Nombre de rayons
Le nombre `N_R` de rayons tracés pour reconstituer une image de taille `N_P` doit être de préférence tel que `N_R` > 0.2 * `N_P`. Ce n'est cependant pas forcément possible du fait de la mémoire vive limitée.

En pratique, de fortes contraintes physiques, notamment la radioactivité des rayons et leur largeur (non nulle), limitent fortement ce nombre de rayons.

### Image initiale utilisée
J'ai considéré quatre images initiales possibles : trois uniformes - une noire, une grise, une blanche - et une "approchée" disponible avec les images cibles (concrètement, l'image initiale est ici l'image cible fortement floutée avec Pillow).

Initialiser l'algorithme avec une image approchée de ce que l'on attend permet d'améliorer la précision de l'image reconstituée.

### Schéma d'accès des rayons
Le schéma d'accès des rayons est l'ordre dans lequel on considère les rayons. J'ai exploré trois options : soit on prend les rayons successivement dans l'ordre dans lequel ils ont été tracés, soit on les prend aléatoirement uniformémement, soit on les prend aléatoirement de manière pondérée (avec une probabilité égale à la norme de la ligne au carré sur la norme de la matrice au carré).

La première simulation, `simu_schema_acces` étudie le comportement asymptotique, après un grand nombre d'itérations de l'algorithme. La deuxième simulation, `simu_vitesse_cv_schema_acces` étudie l'influence du nombre d'itérations en fonction du schéma d'accès : les schémas aléatoires convergent légèrement plus vite que le schéma successif, mais l'on n'observe aucune différence notable entre le schéma aléatoire et celui aléatoire pondéré (théoriquement meilleur).

### Nombre d'itérations
L'algorithme converge assez rapidement, 10 cycles suffisent largement à atteindre quasiment l'image reconstruite asymptotiquement.