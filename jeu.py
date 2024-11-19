from niveau import Niveau
from joueur import Joueur

class Jeu:
    def __init__(self):
        self.tentatives = 0

    def jouer(self):
        while True:
            niveau = Niveau()
            joueur = Joueur(niveau)

            while True:
                print("\nNiveau actuel :")
                niveau.afficher()
                print(f"Position : {joueur.x}, {joueur.y}; Vie : {joueur.vie}")

                if joueur.est_arrive():
                    print(f"Félicitations ! Tu as terminé le niveau en {self.tentatives + 1} tentatives.")
                    return

                mouvement = input("Déplace-toi (z = haut, s = bas, q = gauche, d = droite) : ")
                if not joueur.deplacer(mouvement):
                    break

            self.tentatives += 1
            print("Échec, on réessaye !")