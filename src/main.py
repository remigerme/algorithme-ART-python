from cst import Donnees
from rayons import tracer_rayons
from resolution import ART

from numpy.random import rand
from numpy import dot, zeros

def main():
    cst = Donnees(200, 200, 80, 60)
    A = tracer_rayons(cst)
    # Un premier test sur une image aléatoire
    I = rand(40000)
    R = dot(A, I)
    
    f0 = zeros(40000)
    f = ART(f0, A, R, 10000, False, cst)

main()