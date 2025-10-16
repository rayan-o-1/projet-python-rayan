
#### Importations
import pygame
from typing import List

#### Variables globales
# L'ecran du jeu
screen = None
# Les images a utiliser
joueur_sprite = None
tresor_sprite = None
mur_sprite = None
ennemi_sprite = None
ennemi_tresor_sprite = None
bordure_sprite = None
# La taille de chaque case
taille_case = 0

#### Fonctions
def initialiser_jeu (cote : int) -> None :
    """
    Description :
    -------------
    Cette fonction sert a demarrer la fenetre qui affichera votre RPG. Appelez cette fonction
    dans le code de votre jeu, apres la creation de la carte du RPG.

    Parametres :
    ------------
    - cote : Un entier qui exprime le nombre de cases de votre jeu en longueur et en largeur
             (ce doit etre un carre).

    Retours :
    ---------
    - (None) La fonction ne retourne rien. 
    """
    
    # On fait le lien avec les variables globales
    global screen
    global joueur_sprite, tresor_sprite, mur_sprite, ennemi_sprite, bordure_sprite, \
           ennemi_tresor_sprite
    global taille_case
    
    # On initialise le jeu
    pygame.init()
    
    # On definit la taille de la fenetre du jeu
    ECRAN_COTE = 500
    screen = pygame.display.set_mode([ECRAN_COTE, ECRAN_COTE])
    
    # On definit les sprites 
    joueur_sprite = pygame.sprite.Sprite()
    joueur_sprite.surf = pygame.image.load("images/joueur.png")
    mur_sprite = pygame.sprite.Sprite()
    mur_sprite.surf = pygame.image.load("images/mur.png")
    tresor_sprite = pygame.sprite.Sprite()
    tresor_sprite.surf = pygame.image.load("images/tresor.png")
    ennemi_sprite = pygame.sprite.Sprite()
    ennemi_sprite.surf = pygame.image.load("images/ennemi.png")
    bordure_sprite = pygame.sprite.Sprite()
    bordure_sprite.surf = pygame.image.load("images/bordure.png")
    ennemi_tresor_sprite = pygame.sprite.Sprite()
    ennemi_tresor_sprite.surf = pygame.image.load("images/ennemi_tresor.png")
    
    # On definit la taille des sprites
    taille_case = ECRAN_COTE/cote
    joueur_sprite.surf = pygame.transform.scale(joueur_sprite.surf, (taille_case, taille_case))
    mur_sprite.surf = pygame.transform.scale(mur_sprite.surf, (taille_case, taille_case))
    tresor_sprite.surf = pygame.transform.scale(tresor_sprite.surf, (taille_case, taille_case))
    ennemi_sprite.surf = pygame.transform.scale(ennemi_sprite.surf, (taille_case, taille_case))
    bordure_sprite.surf = pygame.transform.scale(bordure_sprite.surf, (taille_case, taille_case))
    ennemi_tresor_sprite.surf = pygame.transform.scale(ennemi_tresor_sprite.surf, (taille_case, taille_case))
    
    
def afficher_jeu(carte : List[List[int]], ennemis : List[List[int]], tresors : List[List[int]], position_joueur : List[int]) -> None :
    """
    Description :
    -------------
    Cette fonction sert a mettre a jour la fenetre qui affichera votre RPG. Appelez cette
    fonction dans le code de votre jeu, a chaque fois que l'affichage doit changer, c'est-a-dire
    a chaque fois que votre personnage se deplace.

    Parametres :
    ------------
    - carte : Le tableau de tableaux d'entiers qui represente les zones libres et les zones murees.
    - ennemis : Le tableau de tableaux d'entiers qui represente les zones avec des ennemis.
    - tresors : Le tableau de tableaux d'entiers qui represente les zones avec des tresors.
    - position_joueur : Le tableau d'entiers qui correspond aux coordonnees du joueur.

    Retours :
    ---------
    - (None) La fonction ne retourne rien. 
    """
    
    # On fait le lien avec les variables globales
    global taille_case
    
    # On recupere les evenements de la fenetre pour qu'elle puisse se mettre a jour
    pygame.event.get()
    
    # On choisit la couleur de fond de la fenetre
    screen.fill((107, 150, 74))
    
    # On parcourt les coordonnees de la carte et on dessine les bons sprites aux bons endroits
    for x in range(len(carte)) :
        for y in range(len(carte[0])) :
            if position_joueur[0] == x and position_joueur[1] == y :
                screen.blit(joueur_sprite.surf, (y * taille_case, x * taille_case))
            elif ennemis[x][y] >= 1 and tresors[x][y] >= 1 :
                screen.blit(ennemi_tresor_sprite.surf, (y * taille_case, x * taille_case))
            elif ennemis[x][y] >= 1 :
                screen.blit(ennemi_sprite.surf, (y * taille_case, x * taille_case))
            elif tresors[x][y] >= 1 :
                screen.blit(tresor_sprite.surf, (y * taille_case, x * taille_case))
            elif (x == 0 or y == 0 or x == len(carte) - 1 or y == len(carte[0]) - 1) and carte[x][y] != 0 :
                screen.blit(bordure_sprite.surf, (y * taille_case, x * taille_case))
            elif carte[x][y] == 1 :
                screen.blit(mur_sprite.surf, (y * taille_case, x * taille_case))
    
    # On met a jour la fenetre
    pygame.display.flip()
    
def quitter_jeu () -> None :
    """
    Description :
    -------------
    Cette fonction sert a fermer la fenetre qui affichera votre RPG. Appelez cette
    fonction dans le code de votre jeu, au moment ou le jeu s'arrete.

    Parametres :
    ------------
    
    Retours :
    ---------
    - (None) La fonction ne retourne rien. 
    """
    
    # On quitte le jeu
    pygame.quit()