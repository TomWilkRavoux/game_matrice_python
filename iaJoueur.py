import numpy as np
import random
from joueur import Joueur
from niveau import Niveau


class IAJoueur(Joueur):

    def __init__(self, niveau):
        super().__init__(niveau)
        self.experience = 0 

    def jouer_coup(self):
        directions = ["d", "s", "d", "z"]                                        # Ordre de priorité : droite, bas, gauche, haut

        for direction in directions:                                             # Essayer les directions qui ne sont pas des obstacles
            new_x, new_y = self.x, self.y

            if direction == "z" and self.x > 0:
                new_x -= 1
            elif direction == "s" and self.x < self.niveau.taille - 1:
                new_x += 1
            elif direction == "q" and self.y > 0:
                new_y -= 1
            elif direction == "d" and self.y < self.niveau.taille - 1:
                new_y += 1
            else:
                continue
            

            if self.niveau.grille[new_x][new_y] != "1":                               # Si la case n'est pas un obstacle, déplacer l'IA
                self.deplacer(direction)
                print(f"IA se trouve en ({self.x}, {self.y}). Tentative de déplacement : {direction}") 
                return True

        for direction in directions:                                                
            new_x, new_y = self.x, self.y
            if direction == "z" and self.x > 0:
                new_x -= 1
            elif direction == "s" and self.x < self.niveau.taille - 1:
                new_x += 1
            elif direction == "q" and self.y > 0:
                new_y -= 1
            elif direction == "d" and self.y < self.niveau.taille - 1:
                new_y += 1
            else:
                continue

            self.deplacer(direction)   
            print(f"IA se trouve en ({self.x}, {self.y}). Tentative de déplacement : {direction}")                                              # Déplacer vers une case obstacle (force le déplacement)
            return True                                                              # Coup joué, même si c'est un obstacle
        


    def q_learning(niveau, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):

        taille = 5 
        actions = ["z", "s", "q", "d"]
        """
            Entraîne l'IA avec l'algorithme Q-learning.
            :param niveau: Instance de la classe Niveau.
            :param episodes: Nombre d'épisodes d'entraînement.
            :param alpha: Taux d'apprentissage.
            :param gamma: Facteur de récompense future.
            :param epsilon: Probabilité d'explorer au lieu d'exploiter.
        """
        Q_table = np.zeros((niveau.taille, niveau.taille, len(actions)))

        for episode in range(episodes):
            joueur = IAJoueur(niveau)
            done = False

            while not done:
                etat = (joueur.x, joueur.y)

                #ACTIONS
                if random.random() < epsilon:
                    action = random.choice(actions)                                 #EXPLORATION
                else:
                    action = actions[np.argmax(Q_table[etat[0], etat[1]])]          #EXPLOTATION    

                #Jouer l'action met observer la rec !
                if not joueur.deplacer(actions):
                    recompense = -10
                elif joueur.est_arrive():
                    recompense += 100
                    done = True
                else: 
                    recompense = 1  

                #Update table Q
                next_etat = (joueur.x, joueur.y)
                action_index = actions.index(action)
                max_q_next = np.max(Q_table[next_etat[0], next_etat[1]])
                Q_table[etat[0], etat[1]] += alpha * (recompense + gamma * max_q_next - Q_table[etat[0], etat[1], action_index])

        return Q_table
    


	# Création d'un niveau
niveau = Niveau(taille=5, densite_obstacle=0.5)
niveau.afficher()

	# Création de l'IA
ia = IAJoueur(niveau)

	# IA joue automatiquement un coup
while not ia.est_arrive():
	ia.jouer_coup()
	niveau.afficher()