from numpy.random import rand
from numpy.linalg import norm
from numpy import zeros
from PIL import Image

# Pour les coordonnées de l'image dans le plan
# on reprend les conventions de Pillow
# (0, 0) en haut à gauche

#                  #
# OUTILS PRATIQUES #
#                  #

def coords_pixel(k, H):
    return (k // H, k % H)

def indice_pixel(x: int, y: int, H):
    return x * H + y

def tronquer(f):
    # Pour avoir des valeurs dans [0, 1]
    for i in range(len(f)):
        f[i] = max(0, min(1, f[i]))

def ecart_moyen(f, g, N_P):
    return norm(f - g, ord = 1) / N_P

def ecart_norme_euc(f, g):
    return norm(f - g, ord = 2)


#                    #
# GENERATION D'IMAGE #
#                    #

def image_grise(N_P):
    I = zeros(N_P, dtype = float)
    for k in range(N_P):
        I[k] = 0.5
    return I

def image_aleatoire(N_P):
    I = rand(N_P)
    return I

#                    #
# TRAITEMENT D'IMAGE #
#                    #

def image_depuis_fichier(fichier):
    # On renvoie le vecteur ainsi que sa taille
    im = Image.open(fichier)
    # On convertit l'image en mode noir et blanc
    if im.mode != "L":
        im = im.convert("L")
    L, H = im.size
    N_R = L * H
    I = zeros(N_R, dtype = float)
    for k in range(N_R):
        x, y = coords_pixel(k, H)
        I[k] = im.getpixel((x, y)) / 255   
    return (I, L, H)

def enregistrer_image(f, L, H, fichier):
    im = Image.new("L", (L, H), color = 0)
    for k in range(L * H):
        x, y = coords_pixel(k, H)
        im.putpixel((x, y), int(f[k] * 255))
    im.save(fichier)