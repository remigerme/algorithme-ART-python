from resolution import ART
from rayons import tracer_rayons
from image import image_depuis_fichier, enregistrer_image, ecart_moyen
from cst import Donnees

from numpy import zeros, dot
from PIL import Image, ImageFilter


def image_uniforme(N_P, c):
    I = zeros(N_P, dtype = float)
    for k in range(N_P):
        I[k] = c
    return I

def main():
    # Paramètres
    N_THETA, N_RHO = 80, 80
    I, L, H = image_depuis_fichier("exemples/lapin_200.png")
    cst = Donnees(L, H, N_THETA, N_RHO)
    chemin = "simulations/varier_initialisation/lapin/"
    nom_fichier = "lapin_200_1e6_{}_{}_uni_alea.png".format(N_THETA, N_RHO)

    # Initialisation
    A = tracer_rayons(cst)
    R = dot(A, I)
    print("Rayons tracés")
    ecarts = {}

    # Image noire
    f0 = image_uniforme(L * H, 0.0)
    f = ART(f0, A, R, int(1e6), True, cst)
    enregistrer_image(f, L, H, chemin + "noire_" + nom_fichier)
    ecarts["noire"] = ecart_moyen(I, f, L * H)
    print("Image noire terminée")

    # Image blanche
    f0 = image_uniforme(L * H, 1.0)
    f = ART(f0, A, R, int(1e6), True, cst)
    enregistrer_image(f, L, H, chemin + "blanche_" + nom_fichier)
    ecarts["blanche"] = ecart_moyen(I, f, L * H)
    print("Image blanche terminée")

    # Image grise
    f0 = image_uniforme(L * H, 0.5)
    f = ART(f0, A, R, int(1e6), True, cst)
    enregistrer_image(f, L, H, chemin + "grise_" + nom_fichier)
    ecarts["grise"] = ecart_moyen(I, f, L * H)
    print("Image grise terminée")

    # Image approchée
    # Pour approcher l'image, on floute l'image cible
    im = Image.open("exemples/lapin_200.png")
    im_flou = im.filter(ImageFilter.BoxBlur(8))
    im_flou.save("exemples/lapin_200_approche.png")
    f0, _, _= image_depuis_fichier("exemples/lapin_200_approche.png")
    f = ART(f0, A, R, int(1e6), True, cst)
    enregistrer_image(f, L, H, chemin + "approchee_" + nom_fichier)
    ecarts["approchee"] = ecart_moyen(I, f, L * H)
    print("Image approchée terminée")

    with open(chemin + "ecarts_200.txt", "w") as f:
        s = ""
        for (cle, val) in ecarts.items():
            s += cle + ": " + str(val) + "\n"
        f.write(s)


if __name__ == "__main__":
    main()
