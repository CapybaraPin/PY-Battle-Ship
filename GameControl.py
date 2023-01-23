import pygame
import random

"""
        ARCHITECTURE
        
--> Grille : 
    > 0 : Null
    > 1 : Bateau placé (GREY)
    > 2 : Loupé, tir dans le vide (WHITE)
    > 3 : Bateau touché (RED)

--> Bateaux : [2,3,3,4,5]

--> Bibliothèques utilisées : pygame, random

"""

class GameControl:

    def __init__(self, window):
        self.run = False
        self.menu = "home"
        self.game_type = None

        self.arrayA = None
        self.arrayB = None
        self.window = window
        self.colors = [(255,255,255), (209, 92, 92), (114, 106, 106)]
        self.image = None
        self.ships = []
        self.axes = []

        self.coord_last_hit = []

        self.ships_p = [2,3,3,4,5]
        self.count = 0



    def displayText(self, texte, x, y, size, font, color):
        """
            Affiche facilement du texte sur la surface pygame, une tache fréquente et redondante avec PyGame.

        :param texte:str: Texte à afficher
        :param x:int: Coordonnées en abscisse
        :param y:int: Coordonnées en ordonnée
        :param size:int: Taille de l'écriture
        :param font:str: Police d'écriture
        """
        if font == "DIMITRI":
            font = pygame.font.Font('assets/fonts/DIMITRI.TTF', size)
        elif font == "ROBOTO":
            font = pygame.font.Font('assets/fonts/ROBOTO.TTF', size)
        text_display = font.render(texte, True, color)
        text_rect = text_display.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_display, text_rect)

    def lunchGame(self):
        """
            Génération des grilles remplies de 0 et génération des bateaux de l'adversaire.
        """

        self.arrayA = self.arrayGeneration()
        self.arrayB = self.arrayGeneration()
        self.generateShips()

    def generateShips(self):

        for i in self.ships_p:
            self.axes.append(self.insertShip(self.ships, i))

    def resetGame(self):
        """
            Supprime les données tel que : Les grilles, les coordonées des bateaux, les axes.
        """

        self.ships = []
        self.axes = []
        self.lunchGame()

    def arrayGeneration(self):
        """
            Génération d'une grille en 10 x 10.
            La liste par compréhension provoquant des bugs, j'ai du préfaire la liste ci-dessous.
        :return: list
        """

        L = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


        """
        for i in range(10):
            L.append([0 for k in range(10)])
        """

        return L

    def generateCoords(self, ship):
        """
            Créer des coordonées pour l'emplacement du bateau.
        """

        D = random.randint(1, 2)

        if D == 1:

            R_x = random.randint(1, 10);  R_y = random.randint(1, 10 - ship)

            coords = [(R_x, R_y)]

            for i in range(ship - 1):
                R_y = R_y + 1
                coords.append((R_x, R_y))

            orientation = "y"

        else:
            R_x = random.randint(1, 10 - ship); R_y = random.randint(1, 10)

            coords = [(R_x, R_y)]
            for i in range(ship - 1):
                R_x = R_x + 1
                coords.append((R_x, R_y))

            orientation = "x"

        return coords, orientation

    def insertShip(self, ships_c, ship):
        """
            Permet l'insertion d'un bateau sur la grille.
        """
        stat = True

        while stat:
            active = self.generateCoords(ship)
            ships_c.append(active[0])

            if self.checkLocation(ships_c[-1]):
                stat = False
                for i in ships_c[-1]:
                    self.arrayB[i[1]-1][i[0]-1] = 1
        return active[1]


    def checkLocation(self, ships_c):
        """
            Vérifie qu'il est bien possible de placer un bateau à cet emplacement.
        """

        for i in ships_c:
            if self.arrayB[i[1] - 1][i[0] - 1] != 0:
                return False
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if 9 >= i[1] + y - 1 >= 0 and 9 >= i[0] + x - 1 >= 0:
                        if self.arrayB[i[1] + y - 1][i[0] + x - 1] != 0:

                            return False
        return True

    def verifWin(self):
        """
            Vérifie un potentiel gagnant dans la partie en fonction de la somme de tous les 1.
        """

        A, B = 0, 0

        for i in self.arrayA:
            for k in i:
                if k == 1:
                    A += 1

        for i in self.arrayB:
            for k in i:
                if k == 1:
                    B += 1

        if B == 0:
            self.run = False; self.menu = "finish"
            self.displayText("Félicitation, vous avez gagné contre l'ordinateur!", 960, 540, 50, "DIMITRI", self.colors[0])
        elif A == 0:
            self.run = False; self.menu = "finish"
            self.displayText("Dommage vous avez perdu contre l'ordinateur! Retentez votre chance...", 960, 540, 50, "DIMITRI", self.colors[0])


    def attack(self):
        """
            Attaque de l'ordinateur en fonction de plusieurs valeurs :
                > L'attaque easy : l'IA attaque la grille de façon complémente aléatoire.
                > L'attaque normal : l'IA attaque la grille de façon aléatoire puis essaye de terminer la bateau.
                > L'attaque extreme : l'IA touche un bateau avec une chance de 1/3
        """

        if self.game_type == "easy":
            R_x = random.randint(0,9)
            R_y = random.randint(0,9)

            if self.arrayA[R_y][R_x] == 1:
                self.updateCase(R_x, R_y, 3, "A")

            elif self.arrayA[R_y][R_x] == 2 or self.arrayA[R_y][R_x] == 3:
                self.attack()
            else:
                self.updateCase(R_x, R_y, 2, "A")

        elif self.game_type == "extreme":

            R = random.randint(0,3); stat = False

            if R == 3:
                for y in range(10):
                    for x in range(10):
                        if stat == False:
                            if self.arrayA[y][x] == 1:
                                self.updateCase(x, y, 3, "A")
                                stat = True
            else:
                R_x = random.randint(0,9)
                R_y = random.randint(0,9)

                if self.arrayA[R_y][R_x] == 1:
                    self.updateCase(R_x, R_y, 3, "A")

                elif self.arrayA[R_y][R_x] == 2 or self.arrayA[R_y][R_x] == 3:
                    self.attack()

                else:
                    self.updateCase(R_x, R_y, 2, "A")

        elif self.game_type == "normal":
            R_x = random.randint(0, 9)
            R_y = random.randint(0, 9)
            lh = self.coord_last_hit

            if lh == []:
                if self.arrayA[R_y][R_x] == 1:
                    self.updateCase(R_x, R_y, 3, "A")
                    self.coord_last_hit = (R_y, R_x)

                elif self.arrayA[R_y][R_x] == 2 or self.arrayA[R_y][R_x] == 3:
                    self.attack()
                else:
                    self.updateCase(R_x, R_y, 2, "A")

            else:
                for i in range(lh[0] - 1, lh[0] + 1):
                    for j in range(lh[1] - 1, lh[1] + 1):
                        if self.arrayA[i][j] == 1 and (i, j) != lh:
                            self.updateCase(j, i, 3, "A")
                            self.coord_last_hit = (i, j)
                            break
                        else:
                            self.coord_last_hit = []

    def displayArray(self, L):
        """
            Affichage en console d'une grille (principalement pour du débogage)
        """

        print('   A '+' B '+ ' C '+' D '+' E '+' F '+' G '+' H '+' I '+' J')

        if len(L) == 10:
            for i in range(len(L)):
                print(i+1, L[i])
        else:
            print("Erreur : Le tableau n'est pas complet.")

    def placement(self, grid):
            """
                Cette méthode permet à l'utilisateur de placer ses bateaux sur la grille.

            :param:grid:list: Grille de placement.
            """

            grid_size = grid[0]
            grid_width = grid[1]
            grid_height = grid[2]

            for y in range(grid_size):
                for x in range(grid_size):

                    if self.arrayA[y][x] == 0:
                        rect = pygame.Rect(x * grid_width + 70, y * grid_height + 70, grid_width, grid_height)
                        pygame.draw.rect(self.window, self.colors[0], rect, 2)

                    elif self.arrayA[y][x] == 1:
                        rect = pygame.Rect(x * grid_width + 70, y * grid_height + 70, grid_width, grid_height)
                        pygame.draw.rect(self.window, self.colors[2], rect, 50)

            for i in range(5):

                ship = self.ships_p[-1]

                self.displayText(f"Placez un bateau de {ship} cases.", 1300, 400, 50, "DIMITRI", self.colors[0])
                self.displayText(f"Il vous reste {ship-self.count} case(s) à placer.", 1300, 450, 50, "DIMITRI", self.colors[0])

                if self.count < ship:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            running = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()

                            coord_grid = [(70, 770), (70, 770)]

                            if self.mouseClick(mouse_pos, coord_grid):
                                grid_x = mouse_pos[0] // grid_width
                                grid_y = mouse_pos[1] // grid_height

                                rect = pygame.Rect(grid_x * grid_width, grid_y * grid_height, grid_width, grid_height)
                                pygame.draw.rect(self.window, self.colors[0], rect, 50)

                                x = int(rect[0] / 70 - 1)
                                y = int(rect[1] / 70 - 1)

                                if self.arrayA[y][x] != 1:
                                    self.count += 1
                                    self.interClick(rect, "A")

                else:
                    if len(self.ships_p) != 1:
                        self.ships_p.pop();
                        self.count = 0;
                    else:
                        self.run = True
                        self.displayArray(self.arrayA)

                pygame.display.flip()

    def mouseClick(self, mouse_pos, image_coord):
        """
            Détecte si l'utilisateur clique sur une image à partir de coordonnées. (Return TRUE / FALSE)
        """

        return mouse_pos[0] > image_coord[0][0] and mouse_pos[0] < image_coord[0][1] and mouse_pos[1] > image_coord[1][0] and mouse_pos[1] < image_coord[1][1]

    def interClick(self, rect, team):
        """
            Interprète le clique de l'utilisateur dans une case pour le traduire en un potentiel ID dans une liste, puis en fonction de la valeur d'orgine la changer via UpdateCase.
        """
        x = int(rect[0] / 70 -1)
        y = int(rect[1] / 70 -1)

        if team == "A":
            if self.arrayA[y][x] == 0:
                self.updateCase(x, y, 1, "A")

            elif self.arrayA[y][x] == 1:
                self.updateCase(x, y, 3, "A")
        else:
            if self.arrayB[y][x] == 0:
                self.updateCase(x, y, 2, "B")

            elif self.arrayB[y][x] == 1:
                self.updateCase(x, y, 3, "B")


    def updateCase(self, x, y, to, array):
        """
            Met à jour une case, dans une liste via plusieurs paramètres.

        :param x: int: Coordonnées en abscisse
        :param y: int: Coordonnées en ordonnée
        :param to: int: Nouvelle valeur
        :param array: list: Tableau à mettre à jour.
        """

        if array == "A":
            temp = self.arrayA
            temp[y][x] = to
            self.setArrayA(temp)

        elif array == "B":
            temp = self.arrayB
            temp[y][x] = to
            self.setArrayB(temp)

    # SET

    def setMenu(self, type):
        self.menu = type

    def setGameType(self, type):
        self.game_type = type
        self.menu = "placement"

    def setArrayA(self, L):
        self.arrayA = L

    def setArrayB(self, L):
        self.arrayB = L

    def setSelectedImage(self, path):
        self.image = path
