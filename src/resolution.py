from numpy import vdot, zeros, where
from numpy.linalg import norm
from random import randint
from image import tronquer


def prochain_rayon(j, N_R, aleatoire):
    # j est le dernier rayon utilisé
    if not aleatoire:
        return (j + 1) % N_R
    j_ = randint(0, N_R - 1)
    while j == j_:
        j_ = randint(0, N_R - 1)
    return j_


def ART(f0, A, R, N_ITER, aleatoire, cst):
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
    for _ in range(N_ITER):
        f = f - vdot(f, N[j]) * N[j] + T[j]
        j = prochain_rayon(j, N_R, aleatoire)
    tronquer(f)
    return f
