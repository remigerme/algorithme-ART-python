# Simulations autour de l'algorithme ART

Ce projet a été réalisé dans le cadre de mon TIPE (projet de classes préparatoires).

On retrouve une implémentation de l'algorithme ART dans `src/resolution.py`. Tous les fichiers python du projet se trouvent dans `src/`.

## Simulations
Le coeur du projet consiste à étudier l'influence de différents paramètres de l'algorithme ART, qu'ils concernent la préparation des données de projection ou l'exécution de l'algorithme. Pour ce faire, j'ai successivement fait varié les paramètres ci-dessous, sur deux images : le "Shepp Logan phantom" (SLP), une image de test standard en tomographie, ainsi qu'une photo de mon lapin. Les images cibles sont disponibles dans `exemples/slp/` et `exemples/lapin/`, et les résultats des simulations se trouvent dans `simulations/`.

### Nombre de rayons
Le nombre `N_R` de rayons tracés pour reconstituer une image de taille `N_P` doit être de préférence tel que `N_R` > 0.2 * `N_P`. Ce n'est cependant pas forcément possible du fait de la mémoire vive limitée. 

### Image initiale utilisée
J'ai considéré quatre images initiales possibles : trois uniformes - une noire, une grise, une blanche - et une "approchée" disponible avec les images cibles (concrètement, l'image initiale est ici l'image cible fortement floutée avec Pillow).

Initialiser l'algorithme avec une image approchée de ce que l'on attend permet d'améliorer la précision de l'image reconstituée.

### Schéma d'accès des rayons
Le schéma d'accès des rayons est l'ordre dans lequel on considère les rayons. J'ai exploré deux options : soit on prend les rayons successivement dans l'ordre dans lequel ils ont été tracés, soit on les prend aléatoirement.

La première simulation, `simu_schema_acces` étudie le comportement asymptotique, après un grand nombre d'itérations de l'algorithme. La deuxième simulation, `simu_vitesse_cv_schema_acces` étudie l'influence du nombre d'itérations en fonction du schéma d'accès : le schéma aléatoire est théoriquement censé converger plus vite que le schéma successif, mais l'on n'observe pas ce phénomène ici.

### Nombre d'itérations
Il semble qu'itérer l'algorithme continue d'améliorer la précision de l'image reconstituée, même après un grand nombre de cycles réalisés (un cycle = `N_R` itérations de l'algorithme, où `N_R` est le nombre de rayons tracés). Il semblerait qu'il soit très rentable de réaliser au moins 40 cycles.
