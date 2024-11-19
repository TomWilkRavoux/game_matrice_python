import random

class Joueur:
    def __init__(self, niveau):
        self.niveau = niveau
        self.x = 0
        self.y = 0
        self.vie = 3
        self.niveau.grille[self.x][self.y] = "P"

    def deplacer(self, direction):
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
            print("Mouvement invalide.")
            return False

        if self.niveau.grille[new_x][new_y] == "1":  # Si  obstacle
            des = random.randint(1, 6)
            if des <= 3:
                self.vie -= 1
                print("Obstacle ! Tu perds une vie.")
                if self.vie <= 0:
                    print("Game Over. Tu as perdu toutes tes vies !")
                    return False
                return True  # Le joueur bouge pas mais continue jeu

        # Mise à jour de la grille
        self.niveau.grille[self.x][self.y] = str(random.randint(0, 1))  # Remplace ancienne position
        self.x, self.y = new_x, new_y
        self.niveau.grille[self.x][self.y] = "P"

        return True

    def est_arrive(self):
        return self.x == self.niveau.taille - 1 and self.y == self.niveau.taille - 1