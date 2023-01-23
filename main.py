import pygame
from GameControl import *

# Initialisation de pygame
pygame.init()
pygame.display.set_caption("Naval")
window = pygame.display.set_mode((1920,1080))

favicon = pygame.image.load('assets/img/favicon.png')
pygame.display.set_icon(favicon)
pygame.display.flip()

window_x, window_y = window.get_size()

game = GameControl(window)
game.lunchGame()

print("Equipe A:")
game.displayArray(game.arrayA)

print("Equipe B:")
game.displayArray(game.arrayB)

# Définir les couleurs
BLUE = (0, 159, 233)
WHITE = (255, 255, 255)
RED = (209, 92, 92)
GREY = (114, 106, 106)

# Définir les dimensions de la grille
grid_size = 10
grid_width = 700 // grid_size
grid_height = 700 // grid_size

# Chargement des assets
logo = pygame.image.load("assets/img/logo.png")
bouton_play = pygame.image.load("assets/img/bouton_play.png")
easy = pygame.image.load("assets/img/easy.png")
normal = pygame.image.load("assets/img/normal.png")
extreme = pygame.image.load("assets/img/extreme.png")

# Boucle principale
running = True
while running:

    window.fill(BLUE)

    if game.run:
        # JEU

        game.displayText("Grille du joueur adverse :", 325, 35, 40, "DIMITRI", WHITE)

        # Dessiner les lignes de la grille B
        for y in range(grid_size):
            for x in range(grid_size):

                if game.arrayB[y][x] == 0 or game.arrayB[y][x] == 1:
                    rect = pygame.Rect(x * grid_width +70, y * grid_height +70, grid_width, grid_height)
                    pygame.draw.rect(window, WHITE, rect, 2)

                elif game.arrayB[y][x] == 2:
                    rect = pygame.Rect(x * grid_width +70, y * grid_height +70, grid_width, grid_height)
                    pygame.draw.rect(window, WHITE, rect, 50)

                elif game.arrayB[y][x] == 3:
                    rect = pygame.Rect(x * grid_width +70, y * grid_height +70, grid_width, grid_height)
                    pygame.draw.rect(window, RED, rect, 50)

        game.displayText("Votre grille : ", 1290, 35, 40, "DIMITRI", WHITE)

        # Dessiner les lignes de la grille A
        for y in range(grid_size):
            for x in range(grid_size):

                if game.arrayA[y][x] == 0:
                    rect = pygame.Rect(x * grid_width + 1150, y * grid_height + 70, grid_width, grid_height)
                    pygame.draw.rect(window, WHITE, rect, 2)

                elif game.arrayA[y][x] == 1:
                    rect = pygame.Rect(x * grid_width + 1150, y * grid_height + 70, grid_width, grid_height)
                    pygame.draw.rect(window, GREY, rect, 50)

                elif game.arrayA[y][x] == 2:
                    rect = pygame.Rect(x * grid_width + 1150, y * grid_height + 70, grid_width, grid_height)
                    pygame.draw.rect(window, WHITE, rect, 50)

                elif game.arrayA[y][x] == 3:
                    rect = pygame.Rect(x * grid_width + 1150, y * grid_height + 70, grid_width, grid_height)
                    pygame.draw.rect(window, RED, rect, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                grid_x = mouse_pos[0] // grid_width
                grid_y = mouse_pos[1] // grid_height

                if mouse_pos[0] <= 770 and mouse_pos[0] >= 70 and mouse_pos[1] >= 70 and mouse_pos[1] <= 770:

                    rect = pygame.Rect(grid_x * grid_width, grid_y * grid_height, grid_width, grid_height)
                    pygame.draw.rect(window, WHITE, rect, 50)

                    game.verifWin()
                    game.interClick(rect, "B")

                    game.attack()
                    game.verifWin()
        pygame.display.flip()

    else:
        """
            Le menu comporte plusieurs sections : 
                > "home" : La page d'acceuil
                > "choice" : L'utilisateur est invité à choisir la difficulté
                > "placement" : L'utilisateur place ses bateaux
                > "finish" : Annonce des résultats
        """

        if game.menu == "home":

            logo = pygame.transform.scale(logo, (5786 / 10, 4320 / 10))
            window.blit(logo, (1920/2-5786 / 20, 0))

            game.displayText("Battle ship", 960, 500, 120, "DIMITRI", WHITE)
            game.displayText("créé par Hugo ROBLES", 1080, 600, 40, "DIMITRI", WHITE)

            coord_image = [(775,1170), (700, 900)]
            window.blit(bouton_play, (coord_image[0][0], coord_image[1][0]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.mouseClick(pygame.mouse.get_pos(), coord_image):
                        game.setMenu("choice")

            pygame.display.flip()

        elif game.menu == "choice":

            coord_image_easy, coord_image_normal, coord_image_extreme = [(323, 700), (300, 410)], [(770, 1150), (300, 410)], [(1230, 1600), (300, 410)]

            window.blit(easy, (coord_image_easy[0][0], coord_image_easy[1][0]))
            window.blit(normal, (coord_image_normal[0][0], coord_image_normal[1][0]))
            window.blit(extreme, (coord_image_extreme[0][0], coord_image_extreme[1][0]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # JEU FACILE
                    if game.mouseClick(pygame.mouse.get_pos(), coord_image_easy):
                        game.setGameType("easy")

                    # JEU NORMAL
                    if game.mouseClick(pygame.mouse.get_pos(), coord_image_normal):
                        game.setGameType("normal")

                    # JEU EXTREME
                    if game.mouseClick(pygame.mouse.get_pos(), coord_image_extreme):
                        game.setGameType("extreme")

            game.displayText("Choisissez la difficulté du jeu :", 960, 200, 50, "DIMITRI", WHITE)
            game.displayText("Facile : L'ordinateur tirer de manière aléatoire sur votre grille.", 960, 500, 25, "ROBOTO", WHITE)
            game.displayText("Normal : Si l'ordinateur a le malheur de tomber sur votre bateau, il essaye de le terminer !", 960, 550, 25, "ROBOTO", WHITE)
            game.displayText("Extreme : Vous avez une chance sur trois que l'ordinateur touche votre bateau.", 960, 600, 25, "ROBOTO", WHITE)

            pygame.display.flip()

        elif game.menu == "placement":

            game.displayText("Placez vos bateaux sur la grille : ", 410, 40, 40, "DIMITRI", WHITE)

            game.placement([grid_size, grid_width, grid_height])

            pygame.display.flip()

        elif game.menu == "finish":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            game.verifWin()
            pygame.display.flip()

pygame.quit()