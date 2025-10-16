
#Projet RPG
#author :Rayan O

import random
import pygame_min
from typing import List
from random import randint
import pygame
from pygame.locals import *

murs = [[1 , 1 , 1 , 1 , 0 , 1 , 1 , 1 , 1 , 1] , \
[1 , 0 , 1 , 0 , 0 , 0 , 1 , 0 , 0 , 1] , \
[1 , 0 , 1 , 1 , 0 , 1 , 1 , 1 , 0 , 1] , \
[1 , 0 , 1 , 0 , 0 , 1 , 0 , 0 , 0 , 1] , \
[1 , 0 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 1] , \
[1 , 0 , 1 , 0 , 1 , 0 , 0 , 1 , 0 , 1] , \
[1 , 0 , 0 , 0 , 1 , 0 , 1 , 1 , 0 , 1] , \
[1 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 1 , 1] , \
[1 , 1 , 0 , 0 , 1 , 0 , 0 , 0 , 0 , 1] , \
[1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1]]

ennemis = [[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]]

tresors = [[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 1 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0] , \
[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]]

def il_y_a_un_mur ( x :int , y : int ) -> bool :
   
    if murs[x][y] == 1 :
        print("il y'a un murs tu dois bouger!")
        return True
    else :
        return False
"""
    Description :
    -Ce code permet de dire a notre joueur si il y a un mur face a lui
    (un mur vaut 1).

    Paramètres :
    -x : int, y : int

    Retour :
    -Un bool, True si le joueur est face a un mur, False sinon
    """
    
def il_y_a_un_ennemi ( x :int , y : int ) -> bool :
    
    if ennemis[x][y] == 1 :
        print("WOW, cet ennemis est trés puissant  !")
        return True
    else :
        return False
"""
    Description :
    -Ce code permet de dire a notre joueur si il y a un ennemi face a lui
    (un ennemi vaut 1).

    Paramètres :
    -x : int, y : int

    Retour :
    -Un bool, True si le joueur est face a un ennemi, False sinon
    """
    
def il_y_a_un_tresor ( x :int , y : int ) -> bool :
   
    if tresors [x][y] == 1 :
        print("BIENS JOUER tu a trouver un trésore")
        return True
    else :
        return False
"""
    Description :
    -Ce code permet de dire a notre joueur si il y a un trésor face a lui
    (un tresor vaut 1).

    Paramètres :
    -x : int, y : int

    Retour :
    -Un bool, True si le joueur est face a un trésor, False sinon
    """
    
position_joueur = [5, 5]
position_precedente_joueur = [5, 5]

def obtenir_position_joueur () -> List [ int ] :
    return position_joueur
"""
    Description :
    -Cette fonction permet de connaitre la position du joueur.
    
    Parametre :
    -aucun
    
    Retour :
    -Une liste d'entier
    """

def deplacer_joueur ( x : int , y : int ) -> None :
    global position_joueur
    global position_precedente_joueur
    
    # Tu mets a jour la position precedente
    position_precedente_joueur = position_joueur
    
    # Tu changes la position actuelle du joueur
    position_joueur = [x, y]
    print(position_joueur)
    arriver_case()

"""
    Description :
    -Cette fonction permet de deplacer le joueur
    
    Parametre :
    x et y, deux entiers
    
    Retour :
    -Aucun
    """
#fonction trésore#
tresors_collectes = 0


def arriver_case () -> None :
#conceuence si arriver sur trésore    
    if tresors == position_joueur :
        print("il y a un trésor sur votre case !")
    elif ennemis == position_joueur :
        print("il y a un ennemi sur votre case !")
    elif murs == position_joueur :
        print("il y a un mur sur votre case !")
        
    x, y = position_joueur
    if tresors_collectes == 1:
        choix = input("Vous avez trouvé un trésor ! Voulez-vous le ramasser ? (oui/non) : ")
        if choix.lower() == "oui":
            ramasser_tresor(x, y)
            return
#conceuence si arriver sur ennemis       
    if ennemis == 1:
        choix = input("Un ennemi se trouve sur votre case ! Voulez-vous l'affronter ? (oui/non) : ")
        if choix == "oui":
            affronter_ennemi
            return
        else:
            reculer()
"""
    Description :
    -Ce code permet de savoir il y a quoi sur la case du joueur
    Parametre:
    -aucun
    Retour:
    -Rien
    """
arriver_case()

    
#def jouer () -> None :    
#   global position_joueur
 #   x= position_joueur [0]
  #  deplacer_joueur (x , y )
   # pygame_min.quitter_jeu()

#def afficher_histoire():
 #   histoire = """
  #  l histoire
   # """
    #print(histoire)
   
sortie = [0, 4]

def sortir() -> None :
    print("Le jeu est términé, bien joué soldat !")
"""
    Description :
    -Cette fonction permet de terminer le jeu
    Parametre :
    -aucun
    Retour :
    -Rien
    """
    
        

def reculer () -> None :
    revenir = 0
    choix = input("Souhaitez-vous revenir a votre position précédente ? (oui/non)")
    if choix == "oui" :
       revenir = position_precedente_joueur
#le mur initoialement égale a 1 ce change en 0       
def detruire_mur ( x : int , y : int ) -> None :
    global murs
    murs[x][y] = 0
"""
    Description :
    -Cette fonction permet de reculer
    Parametre :
    -Aucun
    Retour :
    -Rien
    """

#répetition de cette fonction a cause de bug       
tresors_collectes = 0
#------------

# ici nous avons utiliser deux def ramasser trésor car nopus nous somme inspiré du premier qui fonctionner mais n etai pas assez precis 

#a modif

#------------
def ramasser_tresor ( x : int , y : int ) -> None :
    global tresors_collectes
    tresors[x][y] = 0    
tresors_collectes += 1
#------------

"""
    Description :
    -Cette fonction permet de dire que le joueur a un trésor en plus
    Parametre :
    -x et y, deux entier
    Retour :
    -Rien
    """
"""
    Description :
    -Cette fonction permet de ramasser un trésor
    Parametre :
    -x et y, deux entier
    Retour :
    -Rien
    """
#------------
        
        

ennemis_vaincus = 0

def affronter_ennemi(x: int, y: int) -> bool:
    global ennemis_vaincus
    
    if ennemis_tuer == 1:
        tuer = random.randint(0, 1) == 0
            
        if tuer:
            ennemis_vaincus += 1
            ennemis_vaincus[x][y] = 0
            print("Ennemi vaincu ! Nombre total d'ennemis vaincus :", ennemis_vaincus)
        
        return vaincu
    else:
        print("Aucun ennemi sur cette case.")
        return False
"""
    Description :
    -Cette fonction permet de savoir combien d'ennemis le joueur a vaincu
    Parametre :
    -x et y, deux entier
    Retour :
    -Un bool
    """
#--------------

def obtenir_position_joueur() -> List[int]:
    return position_joueur
"""
    Description :
    -Cette fonction permet d'obtenir la position du joueur
    Parametre :
    -aucun
    Retour :
    -Une liste d'entier
    """

def deplacer_joueur(x, y):
    global position_joueur, position_precedente_joueur
    position_precedente_joueur = position_joueur 
    position_joueur = [x, y]
    arriver_case()
"""
    Description :
    -Cette fonction permet de déplacer le joueur
    Parametre :
    -x et y, deux entier
    Retour :
    -Rien
    """

def reculer() -> None:
    global position_joueur, position_precedente_joueur
    position_joueur = position_precedente_joueur
    print("tu doit reculer, sale nulos ")
"""
    Description :
    -Cette fonction permet de reculer d'une case
    Parametre :
    -aucun
    Retour :
    -Rien
    """

def detruire_mur(x: int, y: int) -> None:
    global murs
    if murs[y][x] == 1:
        murs[y][x] = 0
        print("Vous avez détruit le mur à la position (" + str(x) + ", " + str(y) + "), tu fonce encore dans les mur en 2024 !?!")
    else:
        print("y a un mur devant, mais par la puissance de python tu passe pas(a en faite si tu MAIS LE FAIT PAS)")
"""
    Description :
    -Cette fonction permet de detruire un mur
    Parametre :
    -x et y, deux entier
    Retour :
    -Rien
    """
def affronter_ennemi(x: int, y: int) -> bool:
    # Utilisation de random.randint pour déterminer le résultat
    resultat = random.randint(0, 1)

    if resultat == 1:
        # L'ennemi est vaincu
        global ennemis_vaincus
        ennemis_vaincus += 1
        print("wow gg pr le kill !!!!!")
        return True
    else:
        # L'ennemi n'est pas vaincu
        print("! T'es trop nul, 0 level !!!")
        return False
"""
    Description :
    -Cette fonction permet de ramasser d'affronter un ennemi
    Parametre :
    -x et y, deux entier
    Retour :
    -Un bool, pour connaitre l'issu du combat
    """
# Variable globale pour activer le code de triche
#----------------------------------
code_triche_active = False

def affronter_ennemi(x: int, y: int) -> bool:
    global code_triche_active
    
    if code_triche_active:
        print("Vous avez vaincu l'ennemi ! (code XXOXOOXXP activer)")
        return True
    
    # Combat normal
    resultat = random.randint(0, 1)
    if resultat == 1:
        print('\33[44m' + "Vous avez vaincu l'ennemi !" + '\33[0m')
        return True
    else:
        print("L'ennemi vous a vaincu.")
        return False

# Fonction pour activer le code de triche
def cheat():
    global ennemis
    for x in range(len(ennemis)):
        for i in range(len(ennemis[x])):
            ennemis[x][i]=0
#----------------------------------
def arriver_case():
    pygame_min.afficher_jeu(murs, ennemis, tresors, position_joueur)
    x, y = position_joueur
    
    if il_y_a_un_mur(x, y):
        choix = input("Un mur bloque votre chemin. continuer ? (Oui/Non): ")
        if choix.lower() == 'oui':
            detruire_mur(x, y)
        else:
            print("Vous décidez de ne pas détruire le mur.")
            reculer()
    elif il_y_a_un_ennemi(x, y):
        choix = input("Un ennemi se dresse devant vous. se battre a mort ? (Oui/Non): ")
        if choix.lower() == 'oui':
            if affronter_ennemi(x, y):
                print()
            else:
                print('\33[41m' + "L'ennemi est trop fort il vous a literallemnt EXPLOSER." + '\33[0m')
                reculer()
        else:
            print("Vous décidez de reculer.")
            reculer()
    elif il_y_a_un_tresor(x, y):
        choix = input("Un trésor étincelant attire votre attention. Voulez-vous le ramasser ? (Oui/Non): ")
        if choix.lower() == 'oui':
            ramasser_tresor(x, y)
            print('\x1b[6;30;42m' + "Vous avez ramassé le trésor avec succès !"+ '\x1b[0m')
        else:
            print("Vous décidez de laisser le trésor derrière vous.")
    else:
        print('\33[5m' + "Il n'y a rien d'intéressant ici, continuez votre exploration." + '\33[0m')
        
    deplacement()
#choiw.lower    
"""
    Description :
    -Cette fonction permet de savoir ce qu'il y a sur sa case
    Parametre :
    -aucun
    Retour :
    -Rien
    AKA la partie la plus relou avec les deplacement 
    """

def sortir() -> None:
    global sortie
    print("Félicitations ! Vous avez atteint la sortie du jeu !")
    print("Nombre d'ennemis vaincus :", ennemis_vaincus)
    print("Nombre de trésors collectés :", tresors_collectes)

"""
    Description :
    -Cette fonction permet de terminer le jeu
    Parametre :
    -aucun
    Retour :
    -Rien
    """
def sortir() -> None:
    print("Le jeu est terminé. T'as atteint la sortie! En vrai t'as de la chance ! T'as battu", ennemis_vaincus, "ennemis et collecté ", {tresors_collectes}, "trésors.(Mouais!)")
"""
    Description :
    -Cette fonction permet de terminer le jeu
    Parametre :
    -aucun
    Retour :
    -Rien
"""

rep = ""

def deplacement_sauve() -> None:
    global position_joueur, murs, ennemis, tresors, code_triche_active
    global rep 
    while True:
        nouvelles_coordonnees = position_joueur[:]
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == QUIT:
                en_cours = False
            elif event.type == KEYDOWN:
                # Déplacement du joueur
                if event.key == K_z:  # Touche Z pour monter
                    nouvelles_coordonnees[0] -= 1
                    rep += 'haut'
                elif event.key == K_s:  # Touche S pour descendre
                    nouvelles_coordonnees[0] += 1
                    rep += 'bas'
                elif event.key == K_q:  # Touche Q pour aller à gauche
                    nouvelles_coordonnees[1] -= 1
                    rep += 'gauche'
                elif event.key == K_d:  # Touche D pour aller à droite
                    nouvelles_coordonnees[1] += 1
                    rep += 'droite'
        
                if 1 <= nouvelles_coordonnees[0] < len(murs[0]) - 1 and 1 <= nouvelles_coordonnees[1] < len(murs) - 1:
                    if nouvelles_coordonnees != sortie:
                        deplacer_joueur(nouvelles_coordonnees[0], nouvelles_coordonnees[1])
                        arriver_case()
                    else:
                        sortir()
                        break
                else:
                    print("a gars bouge de la ")
                   

def deplacement() -> None:
    global position_joueur, murs, ennemis, tresors, code_triche_active
    global rep 
    while True:
        deplacement_2 = input("Dans quelle direction souhaitez-vous vous déplacer (gauche, droite, bas, haut) ? ")
        nouvelles_coordonnees = position_joueur[:]
        if deplacement_2 == 'gauche':
            nouvelles_coordonnees[1] -= 1
            rep += 'gauche'
        elif deplacement_2 == 'droite':
            nouvelles_coordonnees[1] += 1
            rep += 'droite'
        elif deplacement_2 == 'bas':
            nouvelles_coordonnees[0] += 1
            rep += 'bas'
        elif deplacement_2 == 'haut':
            nouvelles_coordonnees[0] -= 1
            rep += 'haut'
        else:
            print("Direction non reconnue. Veuillez entrer gauche, droite, bas ou haut.")
            continue
        if 1 <= nouvelles_coordonnees[0] < len(murs[0]) - 1 and 1 <= nouvelles_coordonnees[1] < len(murs) - 1:
            if nouvelles_coordonnees != sortie:
                deplacer_joueur(nouvelles_coordonnees[0], nouvelles_coordonnees[1])
                arriver_case()
            else:
                sortir()
                break
        else:
            print("a gars bouge de la ")
                   
"""
    Description :
    -Cette fonction permet de faire un déplacement
    Parametre :
    -aucun
    Retour :
    -Rien
    
    J EN PEUT PLUS ALED
    
    """            
#--------------Dialogues-------------
condition_case_teste = True
condition_case_ennemi = False
condition_case_tresor = True

#case test#
dialogue_case_teste = ""
if condition_case_teste:
    dialogue_case_teste = """
Il était une fois, un jeune chevalier du nom de Zeldo.Il vivait dans un royaume qui s'appelait Hyrule.Ce royaume semblait paisible.Il était gouverné par un sage roi, mais malheureusement, il avait beaucoup d'ennemis.Un de ces ennemis était rempli de malice, on le nommait : Ganondork ! Il s'en prit au roi et à sa fille, Lunk... Cependant, malgré le désespoir qui surplombait le royaume, notre héros était décidé à abattre ses ennemis
    """

else:
    dialogue_case_teste = "pagan"
print(dialogue_case_teste)

#case enemis#
dialogue_case_ennemi = ""
if condition_case_ennemi:
    dialogue_case_ennemi = "Attention, un ennemi est proche !"
else:
    dialogue_case_ennemi = "Vous êtes tranquille, pas d'ennemi à proximité."
print(dialogue_case_ennemi)

# Dialogues pour une case avec un trésor
dialogue_case_tresor = ""
if condition_case_tresor:
    dialogue_case_tresor = '\33[93m' +"Vous pouvez trouvé un trésor incroyable !" + '\33[0m'
else:
    dialogue_case_tresor = "Rien de spécial, continuez votre exploration."
print(dialogue_case_tresor)





# Appel de la fonction deplacement
def jouer() -> None :
    
    pygame_min.initialiser_jeu(len(murs))
    deplacer_joueur (x , y )
    pygame_min.quitter_jeu()
            # Initialise l'affichage du jeu
            # Affiche l'histoire du jeu
            # On fait le lien avec les variables globales
            # On deplace le joueur sur sa position initiale
x = position_joueur [0]
y = position_joueur [1]
    
    # Quitte l'affichage du jeu proprement
    
jouer()


#j ai pas eu le temps de mettre le code qui bouge seulment avec zqsd grace a pygme A CAUSE DE BUGGGG
#je n ai pas changer la coueleur de fond car je ne trouvait pas la copbinaison de couleur parfaite 
