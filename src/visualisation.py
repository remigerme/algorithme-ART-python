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
        re_moyen = re.compile("moyen : [0-9].[0-9]*")
        re_euc = re.compile("euclidienne : [0-9].[0-9]*")
        ords_moy = re_moyen.findall(s)
        ords_euc = re_euc.findall(s)
        ords_moy = [float(s[8:]) for s in ords_moy]
        ords_euc = [float(s[14:]) for s in ords_euc]
        label = "lapin" if i == 0 else "shepp logan phantom" # valable uniquement ici
        ax1.bar([e * i + k for k in range(4)], ords_moy, width = e, color=couleurs[i], label=label)
        ax2.bar([e * i + k for k in range(4)], ords_euc, width = e, color=couleurs[i], label=label)
    
    # Légende
    fig.suptitle("Écart à l'image cible suivant différentes initialisations\n200*200px, 80*80 rayons, 1e6 itérations", fontsize = 16)
    ax1.set_ylabel("Écart moyen", fontsize = 14)
    ax2.set_ylabel("Écart en norme 2", fontsize = 14)
    ax1.set_xticks([k + len(fichiers) * e / 4 for k in range(4)])
    ax1.set_xticklabels(["noire", "blanche", "grise", "approchée"], fontsize = 12)
    ax2.set_xticks([k + len(fichiers) * e / 4 for k in range(4)])
    ax2.set_xticklabels(["noire", "blanche", "grise", "approchée"], fontsize = 12)
    plt.legend()
    plt.show()

plot_simu_init(["simulations/varier_initialisation/lapin/ecarts_200.txt", "simulations/varier_initialisation/slp/ecarts_200.txt"])
