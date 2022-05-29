import matplotlib.pyplot as plt
import re

def plot_simu_init(fichiers):
    # Initialisation
    fig, (ax1, ax2) = plt.subplots(2, 1)
    e = 0.75 / len(fichiers) # épaisseur des barres

    couleurs = ["red", "blue", "green"]
    if len(fichiers) > len(couleurs):
        raise Exception("Pas assez de couleurs")

    for (i, fichier) in enumerate(fichiers):
        with open(fichier, "r") as f:
            s = f.read()
        re_moyen = re.compile("moyen : (0\.[0-9]*)")
        re_euc = re.compile("euclidienne : ([0-9]+\.[0-9]*)")
        ords_moy = re_moyen.findall(s)
        ords_euc = re_euc.findall(s)
        ords_moy = [float(s) for s in ords_moy]
        ords_euc = [float(s) for s in ords_euc]
        label = "lapin" if i == 0 else "shepp logan phantom" # valable uniquement ici
        ax1.bar([e * i + k for k in range(4)], ords_moy, width = e, color=couleurs[i], label=label)
        ax2.bar([e * i + k for k in range(4)], ords_euc, width = e, color=couleurs[i], label=label)
    
    # Légende
    fig.suptitle("Écart à l'image cible suivant différentes initialisations\n200*200px, 80*80 rayons, schéma aléa, 1e6 itérations", fontsize = 16)
    ax1.set_ylabel("Écart moyen", fontsize = 14)
    ax2.set_ylabel("Écart en norme 2", fontsize = 14)
    ax1.set_xticks([k + len(fichiers) * e / 4 for k in range(4)])
    ax1.set_xticklabels(["noire", "blanche", "grise", "approchée"], fontsize = 12)
    ax2.set_xticks([k + len(fichiers) * e / 4 for k in range(4)])
    ax2.set_xticklabels(["noire", "blanche", "grise", "approchée"], fontsize = 12)
    plt.legend()
    plt.show()


def plot_simu_schema_acces(fichiers):
    # Initialisation
    fig, (ax1, ax2) = plt.subplots(2, 1)
    e = 0.5 / len(fichiers) # épaisseur des barres

    couleurs = ["red", "blue"]

    for (i, fichier) in enumerate(fichiers):
        with open(fichier, "r") as f:
            s = f.read()
        re_moyen = re.compile("moyen : (0\.[0-9]*)")
        re_euc = re.compile("euclidienne : ([0-9]+\.[0-9]*)")
        ords_moy = re_moyen.findall(s)
        ords_euc = re_euc.findall(s)
        ords_moy = [float(s) for s in ords_moy]
        ords_euc = [float(s) for s in ords_euc]
        
        # On regroupe par image, on juxtapose "succ" et "alea"
        for k in range(2):
            if i == 0:
                label = "successif" if k == 0 else "aléatoire"
            else:
                label = None
            ax1.bar([k * e + i], ords_moy[k], width = e, color=couleurs[k], label=label)
            ax2.bar([k * e + i], ords_euc[k], width = e, color=couleurs[k], label=label)

    # Légende
    fig.suptitle("Écart à l'image cible suivant différents schémas d'accès aux rayons\n200*200px, 80*80 rayons, 1e6 itérations, initialisation noire", fontsize = 16)
    ax1.set_ylabel("Écart moyen", fontsize = 14)
    ax2.set_ylabel("Écart en norme 2", fontsize = 14)
    ax1.set_xticks([len(fichiers) * e / 4, 1 + len(fichiers) * e / 4])
    ax1.set_xticklabels(["lapin", "shepp logan phantom"], fontsize = 12) # uniquement ici
    ax2.set_xticks([len(fichiers) * e / 4, 1 + len(fichiers) * e / 4])
    ax2.set_xticklabels(["lapin", "shepp logan phantom"], fontsize = 12)
    plt.legend()
    plt.show()


def plot_simu_nb_rayons(fichiers, labels, tailles):
    # Initialisation
    fig, (ax1, ax2) = plt.subplots(2, 1)
    
    couleurs = ["#8C3C12", "#CF4D18", "#FF541D", "#124295", "#1A5FD8", "#1DADFF"]
    if len(fichiers) > len(couleurs):
        raise Exception("Pas assez de couleurs")

    for (i, fichier) in enumerate(fichiers):
        with open(fichier, "r") as f:
            s = f.read()
        re_absc= re.compile("\((?P<n_t>[0-9]+), (?P<n_r>[0-9]+)\)")
        re_moy = re.compile("moyen : (0\.[0-9]*)")
        re_euc = re.compile("euclidienne : ([0-9]+\.[0-9]*)")
        absc = [int(m.group("n_t")) * int(m.group("n_r")) / tailles[i] for m in re_absc.finditer(s)]
        ords_moy = re_moy.findall(s)
        ords_euc = re_euc.findall(s)
        ords_moy = [float(s) for s in ords_moy]
        ords_euc = [float(s) for s in ords_euc]
        ax1.plot(absc, ords_moy, color=couleurs[i], label=labels[i])
        ax2.plot(absc, ords_euc, color=couleurs[i], label=labels[i])

    # Légende
    fig.suptitle("Écart à l'image cible suivant différents nombres de rayons tracés\n1e6 itérations pour 150x150, 1e5 itérations pour les autres, initialisation noire", fontsize = 16)
    ax1.set_ylabel("Écart moyen", fontsize = 14)
    ax2.set_ylabel("Écart en norme euclidienne", fontsize = 14)
    ax1.set_xlabel("Nombre de rayons tracés / taille de l'image", fontsize = 14)
    ax2.set_xlabel("Nombre de rayons tracés / taille de l'image", fontsize = 14)
    ax1.set_xlim(right = 0.45)
    ax2.set_xlim(right = 0.45)
    plt.legend(fontsize = 12)
    plt.show()

chemin = "simulations/varier_nb_rayons/"
plot_simu_nb_rayons([chemin + "lapin/ecarts_150.txt", chemin + "lapin/ecarts_100.txt", chemin + "lapin/ecarts_50.txt", chemin + "slp/ecarts_150.txt", chemin + "slp/ecarts_100.txt", chemin + "slp/ecarts_50.txt"],
                    ["lapin 150x150", "lapin 100x100", "lapin 50x50", "slp 150x150", "slp 100x100", "slp 50x50"],
                    [150*150, 100*100, 50*50, 150*150, 100*100, 50*50])
