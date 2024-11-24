import numpy as np
import random
import matplotlib.pyplot as plt
from joueur import Joueur
from niveau import Niveau


class IAJoueur(Joueur):

    def __init__(self, niveau):
        super().__init__(niveau)
        self.experience = 0 

    def jouer_coup(self):
        directions = ["d", "s", "d", "z"]                                        # Ordre de priorité : droite, bas, gauche, haut
        etat = (self.x, self.y)

        # Vérification des limites de la Q-Table
        if hasattr(self, 'q_table') and self.q_table is not None:
            try:
                # Récupérer les valeurs Q pour l'état actuel
                valeurs_q = self.q_table[etat[0], etat[1]]

                # Trier les actions par leur valeur Q (de la plus haute à la plus basse)
                indices_tries = np.argsort(valeurs_q)[::-1]  # Tri décroissant
                directions_tries = [directions[i] for i in indices_tries]
            except IndexError:
                print("Erreur : État hors limites de la Q-Table. Fallback sur logique simple.")
                directions_tries = directions
        else:
            print("Q-Table non disponible. Utilisation de la logique par défaut.")
            directions_tries = directions






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
        rewards = []
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
            total_reward = 0

            while not done:
                etat = (joueur.x, joueur.y)

                #ACTIONS
                if random.random() < epsilon:
                    action = random.choice(actions)                                 #EXPLORATION
                else:
                    action = actions[np.argmax(Q_table[etat[0], etat[1]])]          #EXPLOTATION    

                #Jouer l'action met observer la rec !
                if joueur.est_arrive():                                             # Objectif atteint
                    recompense = 100
                    done = True
                elif not joueur.deplacer(action):                                  # Collision obstacle
                    recompense = -10
                elif etat == next_etat:                                            # Revenir sur la même case
                    recompense = -1                                                     
                else:                                                              #Mouvement valide 
                    recompense = 1                                                 

                #Update table Q
                next_etat = (joueur.x, joueur.y)
                action_index = actions.index(action)
                max_q_next = np.max(Q_table[next_etat[0], next_etat[1]])
                Q_table[etat[0], etat[1], action_index] += alpha * (
                    recompense + gamma * max_q_next - Q_table[etat[0], etat[1], action_index]
                )
                # Q_table[etat[0], etat[1]] += alpha * (recompense + gamma * max_q_next - Q_table[etat[0], etat[1], action_index])

                total_reward += recompense

            # Réduction progressive de epsilon
            epsilon = max(0.1, epsilon * 0.99)

            rewards.append(total_reward)
            print(f"Episode {episode + 1}: Récompense totale = {total_reward}")  


        plt.plot(rewards)
        plt.xlabel("Épisodes")
        plt.ylabel("Récompense Totale")
        plt.title("Progression de l'apprentissage")
        plt.show()      
        return Q_table
    


# 	# Création d'un niveau
# niveau = Niveau(taille=5, densite_obstacle=0.5)
# niveau.afficher()

# q_table = IAJoueur.q_learning(niveau, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1)
# print("Q-Table après entraînement :")
# print(q_table)


# 	# Création de l'IA
# ia = IAJoueur(niveau)

# 	# IA joue automatiquement un coup
# while not ia.est_arrive():
# 	ia.jouer_coup()
# 	niveau.afficher()



# Entraînement avec Q-Learning
niveau = Niveau(taille=5, densite_obstacle=0.5)
q_table = IAJoueur.q_learning(niveau, episodes=2000, alpha=0.5, gamma=0.95, epsilon=0.2)
print("Q-Table après entraînement :")
print(q_table)

while True:
    # Initialiser le niveau et l'IA
    niveau = Niveau(taille=5, densite_obstacle=0.5)
    ia = IAJoueur(niveau)

    print("Nouvelle partie !")
    niveau.afficher()

    # Boucle pour jouer le jeu
    while not ia.est_arrive():
        if ia.vie <= 0:
            print("Game Over. Relancement du jeu...")
            break  # Sortir de la boucle interne pour réinitialiser le jeu
        ia.jouer_coup()
        niveau.afficher()

    # Vérifier si l'IA a gagné
    if ia.est_arrive():
        print("Félicitations ! L'IA a atteint la cible.")
        break  # Sortir de la boucle principale pour terminer le jeu
