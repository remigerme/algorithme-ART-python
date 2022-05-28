from termios import N_MOUSE
from resolution import ART
from rayons import tracer_rayons
from image import image_depuis_fichier, enregistrer_image, ecart_moyen, ecart_norme_euc
from cst import Donnees

from numpy import zeros, dot

"""
Pour cette simulation, on prendra des images de taille 150px par 150px.
En effet, pour des images de 200px par 200px, le programme se fait
systématiquement "tuer" si l'on utilise un nombre trop grand de rayons (>90*90).
"""


def main():
    # Paramètres
    liste_n_theta = list(range(10, 101, 5))
    liste_n_rho = list(range(10, 101, 5))
    n = len(liste_n_theta)
    assert(n == len(liste_n_rho)) # on parcourt simultanément les deux listes avec un compteur
    I, L, H = image_depuis_fichier("exemples/lapin/lapin_150.png")
    chemin = "simulations/varier_nb_rayons/lapin/"
    ecarts = {}

    for i in range(n):
        N_THETA = liste_n_theta[i]
        N_RHO = liste_n_rho[i]
        cst = Donnees(L, H, N_THETA, N_RHO)
        nom_fichier = "lapin_150_1e6_{}_{}_uni.png".format(N_THETA, N_RHO)
        A = tracer_rayons(cst)
        R = dot(A, I)

        f0 = zeros(L * H)
        f = ART(f0, A, R, int(1e6), True, cst)
        enregistrer_image(f, L, H, chemin + nom_fichier)
        ecarts[(N_THETA, N_RHO)] = (ecart_moyen(I, f, L * H), ecart_norme_euc(I, f))

        print("Fin de l'itération i={}".format(i))
    
    with open(chemin + "ecarts_150.txt", "w") as f:
        s = ""
        for (cle, val) in ecarts.items():
            s += str(cle) + ": moyen : " + str(val[0]) + " - norme euclidienne : " + str(val[1])+ "\n"
        f.write(s)


if __name__ == "__main__":
    main()
