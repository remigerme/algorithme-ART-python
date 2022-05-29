from resolution import prochain_rayon
from image import ecart_moyen, ecart_norme_euc, enregistrer_image, tronquer, image_depuis_fichier
from cst import Donnees
from rayons import tracer_rayons

from numpy import zeros, vdot, where, dot, sqrt
from numpy.linalg import norm

from os import listdir
from os.path import isfile, join
import re


def varier_iterations(f0, A, R, N_ITER, sauvegarder_k, aleatoire, cst, chemin):

    fichier = chemin + "{}_{}_{}".format(cst.L, cst.N_THETA, cst.N_RHO)

    def ART_custom(f0, A, R, N_ITER, aleatoire, cst):
        N_R = cst.N_THETA * cst.N_RHO # nombre de rayons
        N_P = cst.L * cst.H # nombre de pixels
        # Les vecteurs normaux aux hyperplans sont les (lignes) A[j]
        # Il est pratique de les rendre unitaires
        # On calcule la norme 1 de chaque ligne
        N = zeros((N_R, N_P))
        normes = norm(A, ord = 1, axis = 1)
        for j in range(N_R):
            N[j] = A[j] / normes[j]
        
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
            j = prochain_rayon(j, N_R, aleatoire)
            if sauvegarder_k(k):
                enregistrer_image(f, cst.L, cst.H, fichier + "_{}.png".format(k))
        tronquer(f)
        return f
    
    f = ART_custom(f0, A, R, N_ITER, aleatoire, cst)
    return f


def simu_iterations(alpha = 0.2):
    # Paramètres
    I, L, H = image_depuis_fichier("exemples/slp/slp_50.png")
    # D'après les courbes du nombre de rayons
    # On prend N_THETA = N_RHO tels que
    # N_THETA * N_RHO = alpha * L * H
    # On considère que L = H
    N_THETA = int(sqrt(alpha) * L)
    N_RHO = N_THETA
    cst = Donnees(L, H, N_THETA, N_RHO)
    chemin = "simulations/varier_iterations/slp/"

    # Initialisation
    A = tracer_rayons(cst)
    R = dot(A, I)
    print("Rayons tracés")
    f0 = zeros(L * H)

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

    # On fait 100 cycles
    varier_iterations(f0, A, R, 100 * N_RHO * N_THETA + 1, sauvegarder_k, True, cst, chemin)


def extraire_stats(fichier_ref, chemin, taille):
    # Valable s'il n'y a qu'une simulation pour l'image de la taille donnée
    I, L, H = image_depuis_fichier(fichier_ref)
    ecarts = {}
    
    fichiers = [f for f in listdir(chemin) if isfile(join(chemin, f))]
    re_filtrer = re.compile("(?P<taille>[0-9]+)_(?P<n_t>[0-9]+)_(?P<n_r>[0-9]+)_(?P<n_iter>[0-9]+)\.png")

    for m in re_filtrer.finditer(" ".join(fichiers)):
        m_taille = int(m.group("taille"))
        m_n_t = int(m.group("n_t"))
        m_n_r = int(m.group("n_r"))
        m_n_iter = int(m.group("n_iter"))
        if m_taille == taille:
            nom_fichier = chemin + "{}_{}_{}_{}.png".format(taille, m_n_t, m_n_r, m_n_iter)
            f, _, _ = image_depuis_fichier(nom_fichier)
            ecarts[m_n_iter] = (ecart_moyen(I, f, L * H), ecart_norme_euc(I, f))

    with open(chemin + "ecarts_{}.txt".format(taille), "w") as f:
        s = ""
        for (cle, val) in ecarts.items():
            s += str(cle) + ": moyen : " + str(val[0]) + " - norme euclidienne : " + str(val[1])+ "\n"
        f.write(s)

extraire_stats("exemples/slp/slp_200.png", "simulations/varier_iterations/slp/", 200)
