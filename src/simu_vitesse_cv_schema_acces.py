from resolution import prochain_rayon
from rayons import tracer_rayons
from image import image_depuis_fichier, enregistrer_image, ecart_moyen, ecart_norme_euc, tronquer
from cst import Donnees

from numpy import zeros, dot, vdot, where
from numpy.linalg import norm

from os import listdir
from os.path import isfile, join
import re


def main():

    # Fonctions auxiliaires
    def sauvegarder_k(k):
        # Si l'on a réalisé moins d'un cycle
        # On sauvegarde tous les "0.2 cycle"
        # Si l'on est entre [10**i, 10**(i + 1)]
        # On sauvegarde tous les "10**i cycles"
        delta_cycle = N_RHO * N_THETA
        n_cycles = k // delta_cycle
        if n_cycles == 0:
            pas = int(0.2 * delta_cycle)
            return k % pas == 0
        elif k % delta_cycle == 0:
            i = 1
            v_i = 10
            while n_cycles > v_i: 
                i += 1
                v_i *= 10
            # Le nombre de cycles est alors dans [10 ** (i - 1), 10**i]
            pas = v_i // 10
            return n_cycles % pas == 0
        return False   

    def ART_custom(f0, A, R, N_ITER, aleatoire, cst, chemin):

        if aleatoire == 0:
            schema_acces = "succ"
        elif aleatoire == 1:
            schema_acces = "alea"
        else:
            schema_acces = "alea_opti"

        fichier = chemin + "{}_{}_{}_{}".format(cst.L, cst.N_THETA, cst.N_RHO, schema_acces)

        N_R = cst.N_THETA * cst.N_RHO # nombre de rayons
        N_P = cst.L * cst.H # nombre de pixels
        # Les vecteurs normaux aux hyperplans sont les (lignes) A[j]
        # Il est pratique de les rendre unitaires
        # On calcule la norme 2 de chaque ligne
        N = zeros((N_R, N_P))
        normes = norm(A, ord = 2, axis = 1)
        for j in range(N_R):
            N[j] = A[j] / normes[j]
        
        # Pour le choix aléatoire optimisé des rayons
        norme_A = norm(A)
        P = [(normes[j] / norme_A) ** 2 for j in range(N_R)]
        les_rayons = list(range(0, N_R))
        
        # On calcule aussi les projections orthogonales de 0 sur les hyperplans
        T = zeros((N_R, N_P))
        for j in range(N_R):
            # On prend h une solution particulière de A[j]h = R[j]
            # Pour ça on prend un coefficient non nul de A[j]
            i0 = where(A[j] > 1e-5)[0][0]
            h = zeros(N_P)
            h[i0] = R[j]
            T[j] = vdot(h, N[j]) * N[j]

        # Initialisation
        f = f0
        j = 0
        for k in range(1, N_ITER + 1):
            f = f - vdot(f, N[j]) * N[j] + T[j]
            j = prochain_rayon(j, N_R, aleatoire, P, les_rayons)
            if sauvegarder_k(k):
                enregistrer_image(f, cst.L, cst.H, fichier + "_{}.png".format(k))
        tronquer(f)
        return f

    # Paramètres
    N_THETA, N_RHO = 60, 60
    I, L, H = image_depuis_fichier("exemples/slp/slp_200.png")
    cst = Donnees(L, H, N_THETA, N_RHO)
    chemin = "simulations/varier_vitesse_cv_schema_acces_bis/slp/"

    # Initialisation
    A = tracer_rayons(cst)
    R = dot(A, I)
    print("Rayons tracés")
    ecarts = {}
    N_ITER = 60 * N_THETA * N_RHO + 1 # 60 cycles
    # Schéma d'accès "successif"
    f0 = zeros(L * H)
    f = ART_custom(f0, A, R, N_ITER, False, cst, chemin)
    print("Image \"successive\" terminée")

    # Schéma d'accès aléatoire
    f0 = zeros(L * H)
    f = ART_custom(f0, A, R, N_ITER, True, cst, chemin)
    print("Image \"aléatoire\" terminée")

    # Schéma d'accès aléatoire amélioré
    f0 = zeros(L * H)
    f = ART_custom(f0, A, R, N_ITER, 2, cst, chemin)
    print("Image \"aléatoire améliorée\" terminée")


def extraire_stats(fichier_ref, chemin, taille):
    # Valable s'il n'y a qu'une simulation pour l'image de la taille donnée
    I, L, H = image_depuis_fichier(fichier_ref)
    ecarts = {}
    
    fichiers = [f for f in listdir(chemin) if isfile(join(chemin, f))]
    re_filtrer = re.compile("(?P<taille>[0-9]+)_(?P<n_t>[0-9]+)_(?P<n_r>[0-9]+)_(?P<alea>succ|alea|alea_opti)_(?P<n_iter>[0-9]+)\.png")

    for m in re_filtrer.finditer(" ".join(fichiers)):
        m_taille = int(m.group("taille"))
        m_n_t = int(m.group("n_t"))
        m_n_r = int(m.group("n_r"))
        m_n_iter = int(m.group("n_iter"))
        m_n_alea = m.group("alea")
        if m_taille == taille:
            nom_fichier = chemin + "{}_{}_{}_{}_{}.png".format(taille, m_n_t, m_n_r, m_n_alea, m_n_iter)
            f, _, _ = image_depuis_fichier(nom_fichier)
            ecarts[(m_n_iter, m_n_alea)] = (ecart_moyen(I, f, L * H), ecart_norme_euc(I, f), m_n_t * m_n_t)

    with open(chemin + "ecarts_{}.txt".format(taille), "w") as f:
        s = ""
        for (cle, val) in ecarts.items():
            s += str(cle[0]) + ": moyen : " + str(val[0]) + " - norme euclidienne : " + str(val[1]) + " - rayons : " + str(val[2]) + " - alea : " + str(cle[1]) + "\n"
        f.write(s)


for image in ["slp", "lapin"]:
    fichier_ref = "exemples/{}/{}_{}.png".format(image, image, 200)
    chemin = "simulations/varier_vitesse_cv_schema_acces_bis/{}/".format(image)
    extraire_stats(fichier_ref, chemin, 200)
