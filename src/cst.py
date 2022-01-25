from dataclasses import dataclass


@dataclass
class Donnees:
    L: int # la largeur de l'image
    H: int # la hauteur de l'image
    N_THETA: int # le nombre d'angles utilisés pour tracer les rayons
    N_RHO: int # le nombre de rayons tracés par angle