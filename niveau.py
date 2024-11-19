import random
import numpy as np

class Niveau:
    def __init__(self, taille=5, densite_obstacle=0.2):
        self.taille = taille
        self.grille = self.generer_niveau()
        self.densite_obstacle = densite_obstacle

    def generer_niveau(self):
        niveau = np.array([[random.randint(0, 1) for _ in range(self.taille)] for _ in range(self.taille)], dtype=str)
        niveau[0][0] = "0"  #case de départ
        return niveau

    def afficher(self):
        for ligne in self.grille:
            print(" ".join(ligne))