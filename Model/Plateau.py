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
    if type(plateau) is not list:
        return False
    if len(plateau) != const.NB_LINES:
        return False
    wrong = "Erreur !"
    if next((wrong for line in plateau if type(line) is not list or len(line) != const.NB_COLUMNS), True) == wrong:
        return False
    if next((wrong for line in plateau for c in line if not (c is None) and not type_pion(c)), True) == wrong:
        return False
    return True


def construirePlateau() -> list:
    """
    Permet de construire un plateau

    :return: Liste de listes représentant un plateau
    """
    plateau = []
    for ligne in range(const.NB_LINES):
        lignePlateau = []
        for colonne in range(const.NB_COLUMNS):
            lignePlateau.append(None)
        plateau.append(lignePlateau)
    return plateau


def placerPionPlateau(plateau: list, pion: dict, numeroColonne: int) -> int:
    """
    Place le pion dans le plateau dans la colonne définie

    :param plateau: Plateau dans lequel on souhaite placer le pion
    :param pion: Pion à placer dans le plateau
    :param numeroColonne: Entier représentant le numéro de la colonne dans laquelle on souhaite placer le pion
    :return: Entier représentant le numéro de la ligne dans laquelle on place le pion, -1 si on ne peut pas le placer
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le deuxième paramètre n'est pas un pion
    :raise TypeError: Si le troisième paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une colonne existante
    """
    if not type_plateau(plateau):
        raise TypeError("placerPionPlateau : Le premier paramètre ne correspond pas à un plateau.")
    if not type_pion(pion):
        raise TypeError("placerPionPlateau : Le second paramètre n'est pas un pion.")
    if type(numeroColonne) is not int:
        raise TypeError("placerPionPlateau : Le troisième paramètre n'est pas un entier.")
    if numeroColonne < 0 or numeroColonne >= const.NB_COLUMNS:
        raise ValueError(f"placerPionPlateau : La valeur de la colonne {numeroColonne} n'est pas correcte.")
    # Si la dernière case de la colonne choisie est vide, on affecte directement le pion
    if plateau[const.NB_LINES - 1][numeroColonne] is None:
        plateau[const.NB_LINES - 1][numeroColonne] = pion
        numLignePion = const.NB_LINES - 1
    # Sinon si la première case de la colonne choisie est remplie, on ne peut pas placer de pion dans la colonne
    elif plateau[0][numeroColonne] is not None:
        numLignePion = -1
    # Sinon, il faut parcourir la colonne de bas en haut pour trouver la place adéquate pour le pion
    else:
        numLignePion = const.NB_LINES - 2  # -2 car on ne reteste pas la dernière case de la colonne
        while numLignePion >= 0 and plateau[numLignePion][numeroColonne] is not None:
            numLignePion -= 1
        plateau[numLignePion][numeroColonne] = pion
    return numLignePion


def toStringPlateau(plateau: list) -> str:
    """
    Transforme le plateau en une chaîne de caractères pour l'afficher visuellement

    :param plateau: Plateau à afficher
    :return: Chaîne de caractères contenant le plateau
    """
    plateauChaineCaractere = ""
    for ligne in range(const.NB_LINES):
        for colonne in range(const.NB_COLUMNS):
            plateauChaineCaractere += "|"
            if plateau[ligne][colonne] is None:
                plateauChaineCaractere += " "
            elif plateau[ligne][colonne][const.COULEUR] == const.ROUGE:
                plateauChaineCaractere += "\x1B[41m \x1B[0m"
            else:  # Il y a un pion qui n'est pas rouge, il est donc jaune
                plateauChaineCaractere += "\x1B[43m \x1B[0m"
        plateauChaineCaractere += "|\n"
    # Ajout par rapport au plateau au format 2D : numérotation des colonnes :
    plateauChaineCaractere += "-" * (const.NB_COLUMNS * 2 + 1) + "\n"
    for i in range(const.NB_COLUMNS):
        plateauChaineCaractere += " " + str(i)
    return plateauChaineCaractere


def detecter4horizontalPlateau(plateau: list, couleur: int) -> list:
    """
    Liste les pions de la couleur choisie alignés par 4 horizontalement

    :param plateau: Plateau à analyser
    :param couleur: Couleur pour laquelle on cherche des pions alignés horizontalement
    :return: Liste des pions de la couleur choisie alignés par 4, une liste vide s'il n'y en a aucun
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4horizontalPlateau : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleur) is not int:
        raise TypeError("detecter4horizontalPlateau : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError("detecter4horizontalPlateau : La valeur de la couleur {couleur} n'est pas correcte.")
    listePion = []
    for ligne in range(const.NB_LINES):
        # Nouvelle ligne : réinitialisation du compteur de pions alignés
        nbPionsAlignes = 0
        for colonne in range(const.NB_COLUMNS):
            # Si on n'est pas sur un pion, ou que ce n'est pas un pion de la bonne couleur
            if plateau[ligne][colonne] is None or plateau[ligne][colonne][const.COULEUR] != couleur:
                # Remise du compteur de pions alignés à 0
                nbPionsAlignes = 0
            # Sinon, c'est un pion de la bonne couleur
            else:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[ligne][colonne-3], plateau[ligne][colonne-2],
                              plateau[ligne][colonne-1], plateau[ligne][colonne]]
                nbPionsAlignes = 0
    return listePion


def detecter4verticalPlateau(plateau: list, couleur: int) -> list:
    """
    Liste les pions de la couleur choisie alignés par 4 verticalement

    :param plateau: Plateau à analyser
    :param couleur: Couleur pour laquelle on cherche des pions alignés verticalement
    :return: Liste des pions de la couleur choisie alignés par 4, une liste vide s'il n'y en a aucun
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4verticalPlateau : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleur) is not int:
        raise TypeError("detecter4verticalPlateau : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError("detecter4verticalPlateau : La valeur de la couleur {couleur} n'est pas correcte.")
    listePion = []
    for colonne in range(const.NB_COLUMNS):
        # Nouvelle colonne : réinitialisation du compteur de pions alignés
        nbPionsAlignes = 0
        for ligne in range(const.NB_LINES):
            # Si on n'est pas sur un pion, ou que ce n'est pas un pion de la bonne couleur
            if plateau[ligne][colonne] is None or plateau[ligne][colonne][const.COULEUR] != couleur:
                # Remise du compteur de pions alignés à 0
                nbPionsAlignes = 0
            # Sinon, c'est un pion de la bonne couleur
            else:
                # On incrémente le compteur de pions alignés de 1
                nbPionsAlignes += 1
            # Si on a 4 pions alignés
            if nbPionsAlignes == 4:
                # On ajoute ces 4 pions à la liste résultat, et on réinitialise le compteur
                listePion += [plateau[ligne-3][colonne], plateau[ligne-2][colonne],
                              plateau[ligne-1][colonne], plateau[ligne][colonne]]
                nbPionsAlignes = 0
    return listePion


def detecter4diagonaleDirectePlateau(plateau: list, couleur: int) -> list:
    """
    Liste les pions de la couleur choisie alignés par 4 sur la diagonale directe

    :param plateau: Plateau à analyser
    :param couleur: Couleur pour laquelle on cherche des pions alignés sur la diagonale directe
    :return: Liste des pions de la couleur choisie alignés par 4, une liste vide s'il n'y en a aucun
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4diagonaleDirectePlateau : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleur) is not int:
        raise TypeError("detecter4diagonaleDirectePlateau : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError("detecter4diagonaleDirectePlateau : La valeur de la couleur {couleur} n'est pas correcte.")
    listePion = []
    # Une diagonale possible ne commence jamais dans les 3 dernières colonnes, ni dans les 3 dernières lignes
    # On parcourt donc toutes les cases de début possibles
    for ligne in range(const.NB_LINES-3):
        for colonne in range(const.NB_COLUMNS-3):
            possible = True
            # Pour chaque case de début, on parcourt la diagonale qui en découle
            for k in range(4):
                # Si une des cases est vide ou n'est pas de la couleur du pion choisi, elle est forcément perdue
                if plateau[ligne+k][colonne+k] is None or plateau[ligne + k][colonne + k][const.COULEUR] != couleur:
                    possible = False
            # Si la diagonale est gagnée, on l'ajoute au résultat !
            if possible:
                listePion += [plateau[ligne][colonne], plateau[ligne+1][colonne+1],
                              plateau[ligne+2][colonne+2], plateau[ligne+3][colonne+3]]
    return listePion


def detecter4diagonaleIndirectePlateau(plateau: list, couleur: int) -> list:
    """
    Liste les pions de la couleur choisie alignés par 4 sur la diagonale indirecte

    :param plateau: Plateau à analyser
    :param couleur: Couleur pour laquelle on cherche des pions alignés sur la diagonale indirecte
    :return: Liste des pions de la couleur choisie alignés par 4, une liste vide s'il n'y en a aucun
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4diagonaleIndirectePlateau : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleur) is not int:
        raise TypeError("detecter4diagonaleIndirectePlateau : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError("detecter4diagonaleIndirectePlateau : La valeur de la couleur {couleur} n'est pas correcte.")
    listePion = []
    # Une anti-diagonale possible ne commence jamais dans les 3 premières colonnes, ni dans les 3 dernières lignes
    # On parcourt donc toutes les cases de début possibles
    for ligne in range(const.NB_LINES - 3):
        for colonne in range(3, const.NB_COLUMNS):
            possible = True
            # Pour chaque case de début, on parcourt l'anti-diagonale qui en découle
            for k in range(0, 4):
                # Si une des cases est vide ou n'est pas de la couleur du pion choisi, elle est forcément perdue
                if plateau[ligne+k][colonne-k] is None or plateau[ligne+k][colonne-k][const.COULEUR] != couleur:
                    possible = False
            # Si l'anti-diagonale est gagnée, on l'ajoute au résultat !
            if possible:
                listePion += [plateau[ligne][colonne], plateau[ligne+1][colonne-1],
                              plateau[ligne+2][colonne-2], plateau[ligne+3][colonne-3]]
    return listePion


def getPionsGagnantsPlateau(plateau: list) -> list:
    """
    Récupère les pions gagnants présents sur le plateau pour toutes les couleurs

    :param plateau: Plateau à analyser
    :return: Liste contenant tous les pions gagnants, une liste vide s'il n'y en a aucun
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if not type_plateau(plateau):
        raise TypeError("getPionsGagnantsPlateau : Le paramètre n'est pas un plateau.")
    # IMPORTANT : On ne fait pas une liste par couleur, mais une liste dans laquelle on met toutes les couleurs
    listePionsGagnants = []
    # On mène les 4 analyses (horizontal, vertical, diagonale, diagonale indirecte) pour chaque couleur
    for couleur in const.COULEURS:
        listePionsGagnants += detecter4verticalPlateau(plateau, couleur)
        listePionsGagnants += detecter4horizontalPlateau(plateau, couleur)
        listePionsGagnants += detecter4diagonaleIndirectePlateau(plateau, couleur)
        listePionsGagnants += detecter4diagonaleDirectePlateau(plateau, couleur)
    return listePionsGagnants


def isRempliPlateau(plateau: list) -> bool:
    """
    Détermine si le plateau passé en paramètre est complètement rempli de pions

    :param plateau: Plateau à analyser
    :return: True si le plateau est intégralement rempli, False sinon
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if not type_plateau(plateau):
        raise TypeError("isRempliPlateau : Le paramètre n’est pas un plateau.")
    res = True
    # Ici, il n'est pas utile de parcourir toutes les lignes : si le plateau n'est pas intégralement rempli,
    # les cases qui sont vides sont forcément le plus haut possible, et donc au moins sur la 1ère ligne
    colonne = 0
    while (colonne < const.NB_COLUMNS) and (res is True):
        if plateau[0][colonne] is None:
            res = False
        colonne += 1
    return res


def placerPionLignePlateau(plateau: list, pion: dict, numLigne: int, left: bool) -> tuple:
    """
    Place le pion dans le plateau dans la ligne définie

    :param plateau: Plateau dans lequel il faut placer le pion
    :param pion: Pion à placer dans le plateau
    :param numLigne: Entier représentant le numéro de la ligne dans laquelle on souhaite placer le pion
    :param left: Booléen à True si on pousse le pion par la gauche, False si on le pousse par la droite
    :return: Un tuple de la liste des pions poussés, et de l'indice de la ligne où le dernier pion poussé se retrouve
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le deuxième paramètre n'est pas un pion
    :raise TypeError: Si le troisième paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une ligne existante
    :raise TypeError: Si le quatrième paramètre n'est pas un bouléen
    """
    if not type_plateau(plateau):
        raise TypeError("placerPionLignePlateau : Le premier paramètre n’est pas un plateau.")
    if not type_pion(pion):
        raise TypeError("placerPionLignePlateau : Le second paramètre n'est pas un pion.")
    if type(numLigne) is not int:
        raise TypeError("placerPionLignePlateau : Le troisième paramètre n'est pas un entier.")
    if numLigne < 0 or numLigne > (const.NB_LINES - 1):
        raise ValueError(f"placerPionLignePlateau : Le troisième paramètre {numLigne} ne désigne pas une ligne.")
    if type(left) is not bool:
        raise TypeError("placerPionLignePlateau : Le quatrième paramètre n'est pas un booléen.")
    listePionPousse = [pion]
    numLignePionRetour = None
    # Si le pion est poussé par la gauche
    if left is True:
        numDernierPionADecaler = 0
        # On parcourt la ligne pour voir jusqu'où on pousse les pions
        while numDernierPionADecaler < const.NB_COLUMNS and plateau[numLigne][numDernierPionADecaler] is not None:
            listePionPousse.append(plateau[numLigne][numDernierPionADecaler])
            numDernierPionADecaler += 1
        # Si le dernier pion poussé est perdu, on affecte le nombre de lignes au retour
        if numDernierPionADecaler == const.NB_COLUMNS:
            numLignePionRetour = const.NB_LINES
        # Sinon si le dernier pion poussé doit "tomber", on cherche à quelle ligne il va le faire
        elif numLigne < (const.NB_LINES - 1) and plateau[numLigne + 1][numDernierPionADecaler] is None:
            numLignePionRetour = const.NB_LINES - 1
            while plateau[numLignePionRetour][numDernierPionADecaler] is not None:
                numLignePionRetour -= 1
            plateau[numLignePionRetour][numDernierPionADecaler] = listePionPousse[len(listePionPousse)-1]
        # Dans les 2 cas ci-dessus, le dernier pion de la liste n'était pas traité dans le déplacement
        # car il était supprimé par remplacement, ou positionné sur une ligne plus basse
        # Sinon, on est pas dans un de ces deux cas et il faut donc penser à décaler TOUS les pions jusqu'à la
        # position indiquée
        else:
            numDernierPionADecaler += 1
        # On parcourt la liste des pions et on les décale tous sur le plateau
        for iPion in range(0, numDernierPionADecaler):
            plateau[numLigne][iPion] = listePionPousse[iPion]
    # Sinon, le pion est poussé par la droite
    else:
        numDernierPionADecaler = const.NB_COLUMNS - 1
        # On parcourt la ligne pour voir jusqu'où on pousse les pions
        while numDernierPionADecaler >= 0 and plateau[numLigne][numDernierPionADecaler] is not None:
            listePionPousse.append(plateau[numLigne][numDernierPionADecaler])
            numDernierPionADecaler -= 1
        # Si le dernier pion poussé est perdu, on affecte le nombre de lignes au retour
        if numDernierPionADecaler == -1:
            numLignePionRetour = const.NB_LINES
        # Sinon si le dernier pion poussé doit "tomber", on cherche à quelle ligne il va le faire
        elif numLigne < (const.NB_LINES - 1) and plateau[numLigne + 1][numDernierPionADecaler] is None:
            numLignePionRetour = const.NB_LINES - 1
            while plateau[numLignePionRetour][numDernierPionADecaler] is not None:
                numLignePionRetour -= 1
            plateau[numLignePionRetour][numDernierPionADecaler] = listePionPousse[len(listePionPousse)-1]
        # Dans les 2 cas ci-dessus, le dernier pion de la liste n'était pas traité dans le déplacement
        # car il était supprimé par remplacement, ou positionné sur une ligne plus basse
        # Sinon, on est pas dans un de ces deux cas et il faut donc penser à décaler TOUS les pions jusqu'à
        # la position indiquée
        else:
            numDernierPionADecaler -= 1
        # On parcourt la liste des pions et on les décale tous sur le plateau
        # for iPion in range(0, numDernierPionADecaler):
        for iPion in range(const.NB_COLUMNS - 1, numDernierPionADecaler, -1):
            plateau[numLigne][iPion] = listePionPousse[const.NB_COLUMNS - 1 - iPion]
    return listePionPousse, numLignePionRetour


def encoderPlateau(plateau: list) -> str:
    """
    Transforme le plateau encodé en chaîne de caractères pour en faire une clé de dictionnaire

    :param plateau: Plateau à encoder
    :return: Chaîne de caractères contenant l'encodage du plateau
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if not type_plateau(plateau):
        raise TypeError("encoderPlateau : Le paramètre ne correspond pas à un plateau.")
    encodagePlateau = ""
    for ligne in range(const.NB_LINES):
        for colonne in range(const.NB_COLUMNS):
            if plateau[ligne][colonne] is None:
                encodagePlateau += "_"
            elif plateau[ligne][colonne][const.COULEUR] == const.ROUGE:
                encodagePlateau += "R"
            else:  # Il y a un pion qui n'est pas rouge, il est donc jaune
                encodagePlateau += "J"
    return encodagePlateau


def isPatPlateau(plateau: list, histogrammesPlateaux: dict) -> bool:
    """
    Evalue si c'est la 5e fois que l'on rencontre le plateau

    :param plateau: Plateau à évaluer
    :param histogrammesPlateaux: Dictionnaire correspondant à "l'histogramme des plateaux"
    :return: True si c'est la 5e fois que l'on rencontre le plateau, False sinon
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le second paramètre n'est pas un dictionnaire
    """
    if not type_plateau(plateau):
        raise TypeError("isPatPlateau : Le premier paramètre n'est pas un plateau.")
    if type(histogrammesPlateaux) is not dict:
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
