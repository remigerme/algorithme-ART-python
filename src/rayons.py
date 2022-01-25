from numpy import array, zeros, linspace, cos, sin, tan, pi


# Pour les coordonnées de l'image dans le plan
# on reprend les conventions de Pillow
# (0, 0) en haut à gauche


def indice_pixel(x: int, y: int, H):
    return x * H + y

def est_valide(x, y, L, H):
    return 0 <= x < L and 0 <= y < H


# On progresse vers la droite
# On sépare le plan en deux
Haut = 0
Bas = 1

# En fonction de la direction, on doit
# vérifier les 3 cases adjacentes
Directions = [
    [(0, -1), (1, -1), (1, 0)],
    [(1, 0), (1, 1), (0, 1)],
]

def rayon_touche_pixel(theta, rho, x, y):
    """
    Attention : ne s'occupe pas de savoir si le pixel est valide
    (x, y) : coordonnées du pixel
    f_k : f(x) avec f : x -> x * tan(theta) + rho / cos(theta)
    l'équation de la droite que parcourt le rayon
    """
    f_k = x * tan(theta) + rho / cos(theta)
    return (f_k < y and f_k + tan(theta) > y) \
            or (f_k > y + 1 and f_k + tan(theta) < y + 1) \
            or (y < f_k < y + 1)


def trouver_premier_pixel(theta, rho, L, H):
    # Renvoie le premier pixel touché ainsi que la direction
    
    # On détermine la direction
    d = Bas if theta < pi / 2 else Haut
    
    # Fonction auxiliaire pour éviter de refaire le calcul de tan(theta)
    def _rayon_touche_pixel(y, f_k):
        return (f_k < y and f_k + tan_theta > y) \
                or (f_k > y + 1 and f_k + tan_theta < y + 1) \
                or (y < f_k < y + 1)
    
    f_k = rho / cos(theta)
    tan_theta = tan(theta)
    for x in range(0, L):
        if x == 0 or x == L - 1:
            # On essaie sur tout le côté de l'image
            for y in range(0, H):
                if _rayon_touche_pixel(y, f_k):
                    return ((x, y), d)
        else:
            # On essaie uniquement aux bords de l'image
            if _rayon_touche_pixel(0, f_k):
                return ((x, 0), d)
            if _rayon_touche_pixel(L - 1, f_k):
                return ((x, L - 1), d)
        f_k += tan_theta
    raise Exception("Un rayon tracé ne passe par aucun pixel, n'est pas censé se produire")


def tracer_rayons(cst):
    # Renvoie la matrice de projection
    N_R = cst.N_THETA * cst.N_RHO
    N_P = cst.L * cst.H
    A = zeros((N_R, N_P), dtype = int)
    e = 0.05 # pour ne pas être trop sur les bords
    
    for (i, theta) in enumerate(linspace(e, pi - e, cst.N_THETA)):
        rho_min = - cst.L * sin(theta)
        rho_max = cst.H * cos(theta)
        tan_theta = tan(theta) # pour éviter de le recalculer plein de fois
        for (j, rho) in enumerate(linspace(rho_min + e, rho_max - e, cst.N_RHO)):
            # Fonction auxiliaire pour éviter de faire trop de calculs
            def _rayon_touche_pixel(y, f_k):
                return (f_k < y and f_k + tan_theta > y) \
                    or (f_k > y + 1 and f_k + tan_theta < y + 1) \
                    or (y < f_k < y + 1)
            # Initialisation
            pas_vus = [True] * N_P # pour ne pas boucler sur des pixels déjà visités
            f_0 = rho / cos(theta)
            ((x, y), d) = trouver_premier_pixel(theta, rho, cst.L, cst.H)
            directions = Directions[d]
            ind = indice_pixel(x, y, cst.H)
            pas_vus[ind] = False
            A[cst.N_RHO * i + j][ind] = 1
            def prochain_pixel(x, y, f_k):
                # On parcourt de proche en proche les pixels
                # On regarde les trois suivants dans le demi-plan qui convient
                for (dx, dy) in directions:
                    x_ = x + dx
                    y_ = y + dy
                    ind = indice_pixel(x_, y_, cst.H)
                    if est_valide(x_, y_, cst.L, cst.H) and pas_vus[ind] and _rayon_touche_pixel(y_, f_k):
                        A[cst.N_RHO * i + j][ind] = 1
                        pas_vus[ind] = False
                        f_k_p = f_k if dx == 0 else f_k + tan_theta
                        prochain_pixel(x_, y_, f_k_p)
            prochain_pixel(x, y, f_0)
    return A
