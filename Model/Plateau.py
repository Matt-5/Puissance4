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
            else:
                plateauChaineCaractere += "\x1B[43m \x1B[0m"
        plateauChaineCaractere += "|\n"
    plateauChaineCaractere += "-" * (const.NB_COLUMNS * 2 + 1) + "\n"
    for i in range(const.NB_COLUMNS):
        plateauChaineCaractere += " " + str(i)
    return plateauChaineCaractere


def detecter4horizontalPlateau(plateau:list, couleur:int)-> list:
    """
    Lister les pions de la couleur choisie qui sont alignés par 4 horizontalement
    :param plateau: Le plateau à analyser
    :param couleur: La couleur pour laquelle on souhaite chercher des pions alignés horizontalement
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
            else:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[ligne][colonne-3], plateau[ligne][colonne-2], plateau[ligne][colonne-1], plateau[ligne][colonne]]
                nbPionsAlignes = 0
            colonne += 1
    return listePion


def detecter4verticalPlateau(plateau:list, couleur:int)-> list:
    """
    Lister les pions de la couleur choisie qui sont alignés par 4 verticalement
    :param plateau: Le plateau à analyser
    :param couleur: La couleur pour laquelle on souhaite chercher des pions alignés verticalement
    :return: La liste des pions de la couleur choisie qui sont alignés par 4, une liste vide s'il n'y en a pas
    :raise TypeError: Si le paramètre n'est pas un plateau
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if type_plateau(plateau) == False:
        raise TypeError("detecter4verticalPlateau : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleur) != int:
        raise TypeError("detecter4verticalPlateau : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError("detecter4verticalPlateau : La valeur de la couleur {couleur} n'est pas correcte.")
    listePion = []
    for colonne in range(const.NB_COLUMNS):
        ligne = const.NB_LINES - 1
        # Nouvelle colonne : réinitialisation du compteur de pions alignés
        nbPionsAlignes = 0
        while ligne >= 0:
            # Si on n'est pas sur un pion, ou que ce n'est pas un pion de la bonne couleur
            if plateau[ligne][colonne] == None or plateau[ligne][colonne][const.COULEUR] != couleur:
                # Remise du compteur de pions alignés à 0
                nbPionsAlignes = 0
            # Sinon, c'est un pion de la bonne couleur
            else:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[ligne+3][colonne], plateau[ligne+2][colonne], plateau[ligne+1][colonne], plateau[ligne][colonne]]
                nbPionsAlignes = 0
            ligne -= 1
    return listePion


def detecter4diagonaleDirectePlateau(plateau:list, couleur:int)-> list:
    """
    Lister les pions de la couleur choisie qui sont alignés par 4 sur la diagonale directe
    :param plateau: Le plateau à analyser
    :param couleur: La couleur pour laquelle on souhaite chercher des pions alignés sur le diagonale directe
    :return: La liste des pions de la couleur choisie qui sont alignés par 4, une liste vide s'il n'y en a pas
    :raise TypeError: Si le paramètre n'est pas un plateau
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if type_plateau(plateau) == False:
        raise TypeError("detecter4diagonaleDirectePlateau : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleur) != int:
        raise TypeError("detecter4diagonaleDirectePlateau : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError("detecter4diagonaleDirectePlateau : La valeur de la couleur {couleur} n'est pas correcte.")
    listePion = []
    # Parcours de la diagonale directe centrale, et de celles situées au-dessus
    for colonne in range(const.NB_COLUMNS - 4, -1, -1):
        i = 0
        # Nouvelle diagonale : réinitialisation du compteur de pions alignés
        nbPionsAlignes = 0
        while i < (const.NB_LINES) and (colonne + i) < const.NB_COLUMNS:
            # Si on n'est pas sur un pion, ou que ce n'est pas un pion de la bonne couleur
            if plateau[i][colonne + i] == None or plateau[i][colonne + i][const.COULEUR] != couleur:
                # Remise du compteur de pions alignés à 0
                nbPionsAlignes = 0
            # Sinon, c'est un pion de la bonne couleur
            else:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[i-3][colonne + (i-3)], plateau[i-2][colonne + (i-2)], plateau[i-1][colonne + (i-1)], plateau[i][colonne + i]]
                nbPionsAlignes = 0
            i += 1
    # Parcours des diagonales directes situées sous la diagonale centrale (qui est exclue du parcours)
    for ligne in range(1, const.NB_LINES - 3):
        i = 0
        # Nouvelle diagonale : réinitialisation du compteur de pions alignés
        nbPionsAlignes = 0
        while i < (const.NB_COLUMNS) and (ligne + i) < const.NB_LINES:
            # Si on n'est pas sur un pion, ou que ce n'est pas un pion de la bonne couleur
            if plateau[ligne + i][i] == None or plateau[ligne + i][i][const.COULEUR] != couleur:
                # Remise du compteur de pions alignés à 0
                nbPionsAlignes = 0
            # Sinon, c'est un pion de la bonne couleur
            else:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[ligne + (i-3)][i-3], plateau[ligne + (i-2)][i-2], plateau[ligne + (i-1)][i-1], plateau[ligne + i][i]]
                nbPionsAlignes = 0
            i += 1
    return listePion

def detecter4diagonaleIndirectePlateau(plateau:list, couleur:int)-> list:
    """
    Lister les pions de la couleur choisie qui sont alignés par 4 sur la diagonale indirecte
    :param plateau: Le plateau à analyser
    :param couleur: La couleur pour laquelle on souhaite chercher des pions alignés sur le diagonale indirecte
    :return: La liste des pions de la couleur choisie qui sont alignés par 4, une liste vide s'il n'y en a pas
    :raise TypeError: Si le paramètre n'est pas un plateau
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if type_plateau(plateau) == False:
        raise TypeError("detecter4diagonaleIndirectePlateau : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleur) != int:
        raise TypeError("detecter4diagonaleIndirectePlateau : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError("detecter4diagonaleIndirectePlateau : La valeur de la couleur {couleur} n'est pas correcte.")
    listePion = []
    # Parcours de la diagonale indirecte centrale et de celles situées au-dessus
    for colonne in range(3, const.NB_COLUMNS):
        i = 0
        # Nouvelle diagonale : réinitialisation du compteur de pions alignés
        nbPionsAlignes = 0
        while i < (const.NB_LINES) and (colonne - i) >= 0:
            # Si on n'est pas sur un pion, ou que ce n'est pas un pion de la bonne couleur
            if plateau[i][colonne - i] == None or plateau[i][colonne - i][const.COULEUR] != couleur:
                # Remise du compteur de pions alignés à 0
                nbPionsAlignes = 0
            # Sinon, c'est un pion de la bonne couleur
            else:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[i-3][colonne - (i-3)], plateau[i-2][colonne - (i-2)], plateau[i-1][colonne - (i-1)], plateau[i][colonne - i]]
                nbPionsAlignes = 0
            i += 1
    # Parcours des diagonales indirectes situées sous la diagonale indirecte centrale (qui est exclue)
    for ligne in range(1, const.NB_LINES - 3):
        i = 0
        # Nouvelle diagonale : réinitialisation du compteur de pions alignés
        nbPionsAlignes = 0
        while 0 <= (const.NB_COLUMNS - 1 - i) and (ligne + i) < const.NB_LINES:
            # Si on n'est pas sur un pion, ou que ce n'est pas un pion de la bonne couleur
            if plateau[ligne + i][const.NB_COLUMNS - 1 - i] == None or plateau[ligne + i][const.NB_COLUMNS - 1 - i][const.COULEUR] != couleur:
                # Remise du compteur de pions alignés à 0
                nbPionsAlignes = 0
            # Sinon, c'est un pion de la bonne couleur
            else:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[ligne + (i-3)][const.NB_COLUMNS - 1 - (i-3)], plateau[ligne + (i-2)][const.NB_COLUMNS - 1 - (i-2)],
                              plateau[ligne + (i-1)][const.NB_COLUMNS - 1 - (i-1)], plateau[ligne + i][const.NB_COLUMNS - 1 - i]]
                nbPionsAlignes = 0
            i += 1
    return listePion


def getPionsGagnantsPlateau(plateau:list)-> list:
    """
    Récupérer les pions gagnants présents sur le plateau pour toutes les couleurs.
    :param plateau: Le plateau à analyser
    :return: La liste contenant tous les pions gagnants, une liste vide sinon
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if type_plateau(plateau) == False:
        raise TypeError("getPionsGagnantsPlateau : Le paramètre n'est pas un plateau.")
    listePionsGagnants = []
    for couleur in const.COULEURS:
        listePionsGagnants += detecter4verticalPlateau(plateau, couleur)
        listePionsGagnants += detecter4horizontalPlateau(plateau, couleur)
        listePionsGagnants += detecter4diagonaleIndirectePlateau(plateau, couleur)
        listePionsGagnants += detecter4diagonaleDirectePlateau(plateau, couleur)
    return listePionsGagnants


def isRempliPlateau(plateau:list)-> bool:
    """
    Déterminer si le plateau passé en paramètre est comlplètement rempli de pions.
    :param plateau: Le plateau à analyser
    :return: True si le plateau est intégralement rempli, False sinon
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if type_plateau(plateau) == False:
        raise TypeError("isRempliPlateau : Le paramètre n’est pas un plateau.")
    res = True
    ligne = 0
    while ligne < const.NB_LINES and res == True:
        colonne = 0
        while colonne < const.NB_COLUMNS and res == True:
            if plateau[ligne][colonne] == None:
                res = False
            colonne += 1
        ligne += 1
    return res


def placerPionLignePlateau(plateau : list, pion : dict, numLigne : int, left : bool) -> tuple:
    """
    Placer le pion dans le plateau dans la ligne définie
    :param plateau: Le plateau dans lequel il faut placer le pion
    :param pion: Le pion à placer
    :param numLigne: Le numéro de la ligne dans laquelle il faut placer le pion
    :param left: True si on pousse le pion par la gauche, False si on le pousse par la droite
    :return: Un tuple constitué de la liste des pions poussés, et de l'indice de la ligne ou le dernier pion poussé se retrouve
    :raise TypeError: Si le paramètre n'est pas un plateau
    :raise TypeError: Si le paramètre n'est pas un pion
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une ligne existante
    :raise TypeError: Si le paramètre n'est pas un bouléen
    """
    if type_plateau(plateau) == False:
        raise TypeError("placerPionLignePlateau : Le premier paramètre n’est pas un plateau.")
    if type_pion(pion) == False:
        raise TypeError("placerPionLignePlateau : Le second paramètre n'est pas un pion.")
    if type(numLigne) != int:
        raise TypeError("placerPionLignePlateau : Le troisième paramètre n'est pas un entier.")
    if numLigne < 0 or numLigne > (const.NB_LINES - 1):
        raise ValueError(f"placerPionLignePlateau : Le troisième paramètre {numLigne} ne désigne pas une ligne.")
    if type(left) != bool:
        raise TypeError("placerPionLignePlateau : Le quatrième paramètre n'est pas un booléen.")
    listePionPousse = [pion]
    numLignePionRetour = None
    # Si le pion est poussé par la gauche
    if left == True:
        numDernierPionADecaler = 0
        # On parcourt la ligne pour voir jusqu'où on pousse les pions
        while numDernierPionADecaler < (const.NB_COLUMNS) and plateau[numLigne][numDernierPionADecaler] != None:
            listePionPousse.append(plateau[numLigne][numDernierPionADecaler])
            numDernierPionADecaler += 1
        # Si le dernier pion poussé est perdu, on affecte le nombre de lignes au retour
        if numDernierPionADecaler == const.NB_COLUMNS:
            numLignePionRetour = const.NB_LINES
        # Sinon si le dernier pion poussé doit "tomber", on cherche à quelle ligne il va le faire
        elif numLigne < (const.NB_LINES - 1) and plateau[numLigne + 1][numDernierPionADecaler] == None:
            numLignePionRetour = const.NB_LINES - 1
            while plateau[numLignePionRetour][numDernierPionADecaler] != None:
                numLignePionRetour -= 1
            plateau[numLignePionRetour][numDernierPionADecaler] = listePionPousse[len(listePionPousse)-1]
        # Dans les 2 cas ci-dessus, le dernier pion de la liste n'était pas traité dans le déplacement
        # car il était supprimé par remplacement, ou positionné sur une ligne plus basse
        # Sinon, on est pas dans un de ces deux cas et il faut donc penser à décaler TOUS les pions jusqu'à la position indiquée
        else:
            numDernierPionADecaler += 1
        # On parcourt la liste des pions et on les décale tous sur le plateau
        for iPion in range(0, numDernierPionADecaler):
            plateau[numLigne][iPion] = listePionPousse[iPion]
    # Sinon, le pion est poussé par la droite
    else:
        numDernierPionADecaler = const.NB_COLUMNS - 1
        # On parcourt la ligne pour voir jusqu'où on pousse les pions
        while numDernierPionADecaler >= 0 and plateau[numLigne][numDernierPionADecaler] != None:
            listePionPousse.append(plateau[numLigne][numDernierPionADecaler])
            numDernierPionADecaler -= 1
        # Si le dernier pion poussé est perdu, on affecte le nombre de lignes au retour
        if numDernierPionADecaler == -1:
            numLignePionRetour = const.NB_LINES
        # Sinon si le dernier pion poussé doit "tomber", on cherche à quelle ligne il va le faire
        elif numLigne < (const.NB_LINES - 1) and plateau[numLigne + 1][numDernierPionADecaler] == None:
            numLignePionRetour = const.NB_LINES - 1
            while plateau[numLignePionRetour][numDernierPionADecaler] != None:
                numLignePionRetour -= 1
            plateau[numLignePionRetour][numDernierPionADecaler] = listePionPousse[len(listePionPousse)-1]
        # Dans les 2 cas ci-dessus, le dernier pion de la liste n'était pas traité dans le déplacement
        # car il était supprimé par remplacement, ou positionné sur une ligne plus basse
        # Sinon, on est pas dans un de ces deux cas et il faut donc penser à décaler TOUS les pions jusqu'à la position indiquée
        else:
            numDernierPionADecaler -= 1
        # On parcourt la liste des pions et on les décale tous sur le plateau
        # for iPion in range(0, numDernierPionADecaler):
        for iPion in range(const.NB_COLUMNS - 1, numDernierPionADecaler, -1):
            plateau[numLigne][iPion] = listePionPousse[const.NB_COLUMNS - 1 - iPion]
    return listePionPousse, numLignePionRetour


def encoderPlateau(plateau : list)-> str:
    """
    Retourner le plateau encodé sous forme de chaîne de caractère
    :param plateau: Le plateau à encoder
    :return: La chaîne de caractère contenant l'encodage du plateau
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if type_plateau(plateau) == False:
        raise TypeError("encoderPlateau : Le paramètre ne correspond pas à un plateau.")
    encodagePlateau = ""
    for ligne in range(const.NB_LINES):
        for colonne in range(const.NB_COLUMNS):
            if plateau[ligne][colonne] == None:
                encodagePlateau += "_"
            elif plateau[ligne][colonne][const.COULEUR] == const.ROUGE:
                encodagePlateau += "R"
            else: # C'est une case contenant un pion jaune
                encodagePlateau += "J"
    return encodagePlateau


def isPatPlateau(plateau : list, histogrammesPlateaux:dict)-> bool:
    """
    Evaluer si c'est la 5e fois que l'on rencontre le plateau
    :param plateau: Le plateau à évaluer
    :param histogrammesPlateaux: Un dictionnaire correspondant à "l'histogramme des plateaux"
    :return: True si c'est la 5e fois que l'on rencontre le plateau, False sinon
    :raise TypeError: Si le paramètre n'est pas un plateau
    :raise TypeError: Si le paramètre n'est pas un dictionnaire
    """
    if type_plateau(plateau) == False:
        raise TypeError("isPatPlateau : Le premier paramètre n'est pas un plateau.")
    if type(histogrammesPlateaux) != dict:
        raise TypeError("isPatPlateau : Le second paramètre n'est pas un dictionnaire.")
    plateauEncode = encoderPlateau(plateau)
    retour = False
    if plateauEncode in histogrammesPlateaux:
        histogrammesPlateaux[plateauEncode] += 1
        if histogrammesPlateaux[plateauEncode] >= 5:
            retour = True
    else:
        histogrammesPlateaux[plateauEncode] = 1
    return retour