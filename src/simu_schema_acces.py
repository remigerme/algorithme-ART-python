from resolution import ART
from rayons import tracer_rayons
from image import image_depuis_fichier, enregistrer_image, ecart_moyen, ecart_norme_euc
from cst import Donnees

from numpy import zeros, dot


def main():
    # Paramètres
    N_THETA, N_RHO = 80, 80
    I, L, H = image_depuis_fichier("exemples/slp/slp_200.png")
    cst = Donnees(L, H, N_THETA, N_RHO)
    chemin = "simulations/varier_schema_acces_bis/slp/"
    nom_fichier = "slp_200_1e6_{}_{}_uni_.png".format(N_THETA, N_RHO)

    # Initialisation
    A = tracer_rayons(cst)
    R = dot(A, I)
    print("Rayons tracés")
    ecarts = {}

    # Schéma d'accès "successif"
    f0 = zeros(L * H)
    f = ART(f0, A, R, int(1e6), 0, cst)
    enregistrer_image(f, L, H, chemin + "succ_" + nom_fichier)
    ecarts["succ"] = (ecart_moyen(I, f, L * H), ecart_norme_euc(I, f))
    print("Image \"successive\" terminée")

    # Schéma d'accès aléatoire
    f0 = zeros(L * H)
    f = ART(f0, A, R, int(1e6), 1, cst)
    enregistrer_image(f, L, H, chemin + "alea_" + nom_fichier)
    ecarts["alea"] = (ecart_moyen(I, f, L * H), ecart_norme_euc(I, f))
    print("Image \"aléatoire\" terminée")

    # Schéma d'accès aléatoire optimisé
    f0 = zeros(L * H)
    f = ART(f0, A, R, int(1e6), 2, cst)
    enregistrer_image(f, L, H, chemin + "alea_opti_" + nom_fichier)
    ecarts["alea_opti"] = (ecart_moyen(I, f, L * H), ecart_norme_euc(I, f))
    print("Image \"aléatoire optimisée\" terminée")

    with open(chemin + "ecarts_200.txt", "w") as f:
        s = ""
        for (cle, val) in ecarts.items():
            s += cle + ": moyen : " + str(val[0]) + " - norme euclidienne : " + str(val[1])+ "\n"
        f.write(s)


if __name__ == "__main__":
    main()
