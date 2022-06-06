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


# plot_simu_init(["simulations/varier_initialisation/lapin/ecarts_200.txt", "simulations/varier_initialisation_bis/slp/ecarts_200.txt"])


def plot_simu_schema_acces(fichiers):
    # Initialisation
    fig, (ax1, ax2) = plt.subplots(2, 1)
    e = 0.5 / len(fichiers) # épaisseur des barres

    couleurs = ["red", "blue", "green"]

    for (i, fichier) in enumerate(fichiers):
        with open(fichier, "r") as f:
            s = f.read()
        re_moyen = re.compile("moyen : (0\.[0-9]*)")
        re_euc = re.compile("euclidienne : ([0-9]+\.[0-9]*)")
        ords_moy = re_moyen.findall(s)
        ords_euc = re_euc.findall(s)
        ords_moy = [float(s) for s in ords_moy]
        ords_euc = [float(s) for s in ords_euc]
        
        # On regroupe par image, on juxtapose "succ", "alea" et "alea_opti"
        for k in range(3):
            if i == 0:
                if k == 0:
                    label = "successif"
                elif k == 1:
                    label = "alea"
                else:
                    label = "alea_opti"
            else:
                label = None
            ax1.bar([k * e + i], ords_moy[k], width = e, color=couleurs[k], label=label)
            ax2.bar([k * e + i], ords_euc[k], width = e, color=couleurs[k], label=label)

    # Légende
    fig.suptitle("Écart à l'image cible suivant différents schémas d'accès aux rayons\n200*200px, 80*80 rayons, 1e6 itérations, initialisation noire", fontsize = 16)
    ax1.set_ylabel("Écart moyen", fontsize = 14)
    ax2.set_ylabel("Écart en norme 2", fontsize = 14)
    ax1.set_xticks([len(fichiers) * e / 2, 1 + len(fichiers) * e / 2])
    ax1.set_xticklabels(["lapin", "shepp logan phantom"], fontsize = 12) # uniquement ici
    ax2.set_xticks([len(fichiers) * e / 2, 1 + len(fichiers) * e / 2])
    ax2.set_xticklabels(["lapin", "shepp logan phantom"], fontsize = 12)
    plt.legend()
    plt.show()


# plot_simu_schema_acces(["simulations/varier_schema_acces_bis/lapin/ecarts_200.txt", "simulations/varier_schema_acces_bis/slp/ecarts_200.txt"])


def plot_simu_vitesse_cv_schema_acces(fichiers, labels):
    # Initialisation
    fig, (ax1, ax2) = plt.subplots(2, 1)
    
    couleurs = ["#8C3C12", "#CF4D18", "#FF541D", "#124295", "#1A5FD8", "#1DADFF"]
    if len(fichiers) > 2 * len(couleurs):
        raise Exception("Pas assez de couleurs")

    for (i, fichier) in enumerate(fichiers):
        with open(fichier, "r") as f:
            s = f.read()
        re_data = re.compile("(?P<n_iter>[0-9]+): moyen : (?P<moy>0\.[0-9]+) - norme euclidienne : (?P<euc>[0-9]+\.[0-9]+) - rayons : (?P<nb_rayons>[0-9]+) - alea : (?P<alea>succ|alea_opti|alea)")
        absc_alea, absc_succ, absc_alea_opti = [], [], []
        ords_moy_alea, ords_euc_alea = [], []
        ords_moy_succ, ords_euc_succ = [], []
        ords_moy_alea_opti, ords_euc_alea_opti = [], []
        for m in re_data.finditer(s):
            if m.group("alea") == "alea":
                absc_alea.append(int(m.group("n_iter")) / int(m.group("nb_rayons")))
                ords_moy_alea.append(float(m.group("moy")))
                ords_euc_alea.append(float(m.group("euc")))
            elif m.group("alea") == "succ":
                absc_succ.append(int(m.group("n_iter")) / int(m.group("nb_rayons")))
                ords_moy_succ.append(float(m.group("moy")))
                ords_euc_succ.append(float(m.group("euc")))
            else:
                absc_alea_opti.append(int(m.group("n_iter")) / int(m.group("nb_rayons")))
                ords_moy_alea_opti.append(float(m.group("moy")))
                ords_euc_alea_opti.append(float(m.group("euc")))
        
        ax1.plot(absc_alea, ords_moy_alea, color=couleurs[3 * i], label=labels[3 * i])
        ax2.plot(absc_alea, ords_euc_alea, color=couleurs[3 * i], label=labels[3 * i])
        ax1.plot(absc_succ, ords_moy_succ, color=couleurs[3 * i + 1], label=labels[3 * i + 1])
        ax2.plot(absc_succ, ords_euc_succ, color=couleurs[3 * i + 1], label=labels[3 * i + 1])
        ax1.plot(absc_alea_opti, ords_moy_alea_opti, color=couleurs[3 * i + 2], label=labels[3 * i + 2])
        ax2.plot(absc_alea_opti, ords_euc_alea_opti, color=couleurs[3 * i + 2], label=labels[3 * i + 2])

    # Légende
    fig.suptitle("Écart à l'image cible suivant le nombre d'itérations effectuées\n60*60 rayons, initialisation noire, 200x200px", fontsize = 16)
    ax1.set_ylabel("Écart moyen", fontsize = 14)
    ax2.set_ylabel("Écart en norme euclidienne", fontsize = 14)
    ax1.set_xlabel("Nombre de cycles", fontsize = 14)
    ax2.set_xlabel("Nombre de cycles", fontsize = 14)
    plt.legend(fontsize = 12)
    plt.show()


# chemin = "simulations/varier_vitesse_cv_schema_acces/"
# plot_simu_vitesse_cv_schema_acces([chemin + "lapin/ecarts_200.txt", chemin + "slp/ecarts_200.txt"],
#                                   ["lapin 200x200 aléatoire", "lapin 200x200 successif", "lapin 200x200 aléatoire opti", "slp 200x200 aléatoire", "slp 200x200 successif", "slp 200x200 aléatoire opti"])



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
    fig.suptitle("Écart à l'image cible suivant différents nombres de rayons tracés\n1e5 itérations, initialisation noire", fontsize = 16)
    ax1.set_ylabel("Écart moyen", fontsize = 14)
    ax2.set_ylabel("Écart en norme euclidienne", fontsize = 14)
    ax1.set_xlabel("Nombre de rayons tracés / taille de l'image", fontsize = 14)
    ax2.set_xlabel("Nombre de rayons tracés / taille de l'image", fontsize = 14)
    ax1.set_xlim(right = 0.45)
    ax2.set_xlim(right = 0.45)
    plt.legend(fontsize = 12)
    plt.show()

chemin = "simulations/varier_nb_rayons_bis/"
plot_simu_nb_rayons([chemin + "lapin/ecarts_50.txt", chemin + "lapin/ecarts_100.txt", chemin + "lapin/ecarts_150.txt", chemin + "slp/ecarts_50.txt", chemin + "slp/ecarts_100.txt", chemin + "slp/ecarts_150.txt"],
                    ["lapin 50", "lapin 100", "lapin 150", "slp 50", "slp 100", "slp 150"],
                    [50*50, 100*100, 150*150, 50*50, 100*100, 150*150])

def plot_simu_nb_iterations(fichiers, labels):
    # Initialisation
    fig, (ax1, ax2) = plt.subplots(2, 1)
    
    couleurs = ["#8C3C12", "#CF4D18", "#FF541D", "#124295", "#1A5FD8", "#1DADFF"]
    if len(fichiers) > len(couleurs):
        raise Exception("Pas assez de couleurs")

    for (i, fichier) in enumerate(fichiers):
        with open(fichier, "r") as f:
            s = f.read()
        re_absc= re.compile("(?P<n_iter>[0-9]+):")
        re_moy = re.compile("moyen : (0\.[0-9]*)")
        re_euc = re.compile("euclidienne : ([0-9]+\.[0-9]*)")
        re_rayons = re.compile("rayons : (?P<nb_rayons>[0-9]+)")
        nb_rayons = [int(m.group("nb_rayons")) for m in re_rayons.finditer(s)]
        absc = [int(m.group("n_iter")) / nb_rayons[i] for m in re_absc.finditer(s)]
        ords_moy = re_moy.findall(s)
        ords_euc = re_euc.findall(s)
        ords_moy = [float(s) for s in ords_moy]
        ords_euc = [float(s) for s in ords_euc]
        ax1.plot(absc, ords_moy, color=couleurs[i], label=labels[i])
        ax2.plot(absc, ords_euc, color=couleurs[i], label=labels[i])

    # Légende
    fig.suptitle("Écart à l'image cible suivant le nombre d'itérations effectuées\nnombre de rayons \"optimal\", initialisation noire", fontsize = 16)
    ax1.set_ylabel("Écart moyen", fontsize = 14)
    ax2.set_ylabel("Écart en norme euclidienne", fontsize = 14)
    ax1.set_xlabel("Nombre de cycles", fontsize = 14)
    ax2.set_xlabel("Nombre de cycles", fontsize = 14)
    ax1.set_xlim(left = -0.1, right = 30)
    ax2.set_xlim(left = -0.1, right = 30)
    plt.legend(fontsize = 12)
    plt.show()

# chemin = "simulations/varier_iterations/"
# plot_simu_nb_iterations([chemin + "lapin/ecarts_50.txt", chemin + "lapin/ecarts_100.txt", chemin + "lapin/ecarts_150.txt", chemin + "slp/ecarts_50.txt", chemin + "slp/ecarts_100.txt", chemin + "slp/ecarts_150.txt"],
#                         ["lapin 50", "lapin 100", "lapin 150", "slp 50", "slp 100", "slp 150"])
