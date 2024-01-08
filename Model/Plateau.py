from Model.Constantes import *
from Model.Pion import *


#
# Le plateau représente la grille où sont placés les pions.
# Il constitue le coeur du jeu car c'est dans ce fichier
# où vont être programmées toutes les règles du jeu.
#
# Un plateau sera simplement une liste de liste.
# Ce sera en fait une liste de lignes.
# Les cases du plateau ne pourront contenir que None ou un pion
#
# Pour améliorer la "rapidité" du programme, il n'y aura aucun test sur les paramètres.
# (mais c'est peut-être déjà trop tard car les tests sont fait en amont, ce qui ralentit le programme...)
#

def type_plateau(plateau: list) -> bool:
    """
    Permet de vérifier que le paramètre correspond à un plateau.
    Renvoie True si c'est le cas, False sinon.

    :param plateau: Objet qu'on veut tester
    :return: True s'il correspond à un plateau, False sinon
    """
    if type(plateau) != list:
        return False
    if len(plateau) != const.NB_LINES:
        return False
    wrong = "Erreur !"
    if next((wrong for line in plateau if type(line) != list or len(line) != const.NB_COLUMNS), True) == wrong:
        return False
    if next((wrong for line in plateau for c in line if not(c is None) and not type_pion(c)), True) == wrong:
        return False
    return True


def construirePlateau()-> list:
    """
    Fonction permettant de construire un plateau
    :return: Tableau 2D représentant un plateau
    """
    plateau = []
    for ligne in range(const.NB_LINES):
        lignePlateau = []
        for colonne in range(const.NB_COLUMNS):
            lignePlateau.append(None)
        plateau.append(lignePlateau)
    return plateau


def placerPionPlateau(plateau:list, pion:dict, numeroColonne:int)-> int:
    """
    Placer le pion dans le plateau dans la colonne définie
    :param plateau: Le pion dans lequel on souhaite placer le pion
    :param pion: Le pion à placer dans le plateau
    :param numeroColonne: Le numéro de la colonne dans laquelle on souhaite placer le pion
    :return: Le numéro de la ligne dans laquelle on place le pion, -1 si on en peut pas le placer
    :raise TypeError: Si le paramètre n'est pas un plateau
    :raise TypeError: Si le paramètre n'est pas un pion
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une colonne existante
    """
    if type_plateau(plateau) == False:
        raise TypeError("placerPionPlateau : Le premier paramaètre ne correspond pas à un plateau.")
    if type_pion(pion) == False:
        raise TypeError("placerPionPlateau : Le second paramètre n'est pas un pion.")
    if type(numeroColonne) != int:
        raise TypeError("placerPionPlateau : Le troisième paramètre n'est pas un entier.")
    if numeroColonne < 0 or numeroColonne >= const.NB_COLUMNS:
        raise ValueError(f"placerPionPlateau : La valeur de la colonne {numeroColonne} n'est pas correcte.")
    if plateau[const.NB_LINES - 1][numeroColonne] == None:
        plateau[const.NB_LINES - 1][numeroColonne] = pion
        numLignePion = const.NB_LINES - 1
    elif plateau[0][numeroColonne] != None:
        numLignePion = -1
    else:
        numLignePion = const.NB_LINES - 2
        while numLignePion >= 0 and plateau[numLignePion][numeroColonne] != None:
            numLignePion -= 1
        plateau[numLignePion][numeroColonne] = pion
    return numLignePion


def toStringPlateau(plateau: list)-> str:
    """
    Afficher le plateau sous forme de chaîne de caractères
    :param plateau: Le plateau à afficher
    :return: La chaîne de caractères contenant l'affichage de plateau
    """
    plateauChaineCaractere = ""
    for ligne in range(const.NB_LINES):
        for colonne in range(const.NB_COLUMNS):
            plateauChaineCaractere += "|"
            if plateau[ligne][colonne] == None:
                plateauChaineCaractere += " "
            elif plateau[ligne][colonne][const.COULEUR] == const.ROUGE:
                plateauChaineCaractere += "\x1B[41m \x1B[0m"
            elif plateau[ligne][colonne][const.COULEUR] == const.JAUNE:
                plateauChaineCaractere += "\x1B[43m \x1B[0m"
        plateauChaineCaractere += "|\n"
    plateauChaineCaractere += "-" * (const.NB_COLUMNS * 2 + 1) + "\n"
    for i in range(const.NB_COLUMNS):
        plateauChaineCaractere += " " + str(i)
    return plateauChaineCaractere


def detecter4horizontalPlateau(plateau:list, couleur:int)-> list:
    """
    Lister les pions de la couleur choisie qui sont alignés par 4
    :param plateau: Le plateau à analyser
    :param couleur: La couleur pour laquelle on souhaite chercher des pions alignés
    :return: La liste des pions de la couleur choisie qui sont alignés par 4, une liste vide s'il n'y en a pas
    :raise TypeError: Si le paramètre n'est pas un plateau
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if type_plateau(plateau) == False:
        raise TypeError("detecter4horizontalPlateau : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleur) != int:
        raise TypeError("detecter4horizontalPlateau : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError("detecter4horizontalPlateau : La valeur de la couleur {couleur} n'est pas correcte.")
    listePion = []
    for ligne in range(const.NB_LINES):
        colonne = 0
        # Nouvelle ligne : réinitialisation du compteur de pions alignés
        nbPionsAlignes = 0
        while colonne < const.NB_COLUMNS:
            # Si on n'est pas sur un pion, ou que ce n'est pas un pion de la bonne couleur
            if plateau[ligne][colonne] == None or plateau[ligne][colonne][const.COULEUR] != couleur:
                # Remise du compteur de pions alignés à 0
                nbPionsAlignes = 0
            # Sinon, c'est un pion de la bonne couleur
            elif plateau[ligne][colonne][const.COULEUR] == couleur:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[ligne][colonne-3], plateau[ligne][colonne-2], plateau[ligne][colonne-1], plateau[ligne][colonne]]
                nbPionsAlignes = 0
            colonne += 1
    return listePion