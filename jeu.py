import time
import sys
import random
from colorama import Fore, init
from niveau import Niveau
from joueur import Joueur



init()

class Jeu:
    def __init__(self):
        self.tentatives = 0

    def menu(self):
        print(Fore.MAGENTA + "Hehe à toi de choisir !! good game !")
        print("---------------------------------------------------")
        print(Fore.GREEN + "1 = Mode classique")
        print("2 = Mode course contre la montre")
        print("3 = Mode difficile")
        print(Fore.MAGENTA + "---------------------------------------------------")
        choix = input(Fore.YELLOW + "Choisissez un mode (1 ,2, 3) :")
        return choix


    def jeu_classique(self):
        while True:
            niveau = Niveau()
            joueur = Joueur(niveau)

            print(Fore.GREEN + "Mode Classique")

            while True:
                print(Fore.YELLOW + "\nNiveau actuel :")
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

    def jeu_timer(self):
        niveau = Niveau()
        joueur = Joueur(niveau)

        print(Fore.GREEN + "\nMode Timer ! Terminez le niveau en moins d'une minute.")

        debut = time.time()
        limite_temps = 15

        while True:
            print(Fore.YELLOW + "\nNiveau actuel :")
            niveau.afficher()
            print(f"Position : {joueur.x}, {joueur.y}; Vie : {joueur.vie}")

            temps_ecoule = time.time() - debut
            temps_restant = limite_temps - temps_ecoule

            if temps_restant <= 0:
                print("⏳ Temps écoulé ! Vous avez perdu.")
                print(f"Votre temps est de {temps_ecoule}")
                return
            
            sys.stdout.write(f"\rTemps restant : {temps_restant:.2f} secondes")
            sys.stdout.flush()
            
            if joueur.est_arrive():
                fin = time.time()  # Arrêter le chronomètre
                temps_total = fin - debut
                print(f"Félicitations ! Tu as terminé le niveau en {temps_total:.2f} secondes.")
                return
            
            mouvement = input("Déplace-toi (z = haut, s = bas, q = gauche, d = droite) : ")
            if not joueur.deplacer(mouvement):
                print("Perdu ! Vous avez rencontré un obstacle fatal.")
                return
            
    def jeu_difficile(self):
        while True:
            niveau = Niveau(taille=10, densite_obstacle=0.4)
            joueur = Joueur(niveau)
            joueur.vie = 1

            print(Fore.GREEN + "Mode Difficile")

            while True:
                print(Fore.YELLOW + "\nNiveau actuel :")
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

    def jouer(self):
        choix = self.menu()

        if choix == "1":
            self.jeu_classique()
        elif choix == "2":
            self.jeu_timer()
        elif choix == "3":
            self.jeu_difficile()
        else:
            print("Choix invalide, veuillez relancer le jeu.")            