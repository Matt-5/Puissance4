from Model.Constantes import *
from Model.Plateau import *
from Model.Joueur import *


def copierPlateau(plateau: list) -> list:
    """
    Copie en profondeur un plateau

    :param plateau: Plateau à copier
    :return: Liste de liste correspondant à une copie profonde du plateau
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    """
    if not type_plateau(plateau):
        raise TypeError("evaluerCoupLigne : Le premier paramètre ne correspond pas à un plateau.")
    copiePlateau = []
    for ligne in range(const.NB_LINES):
        copieLigne = []
        for colonne in range(const.NB_COLUMNS):
            if plateau[ligne][colonne] is None:
                copieLigne.append(None)
            else:
                copieLigne.append(plateau[ligne][colonne].copy())
        copiePlateau.append(copieLigne)
    return copiePlateau


def evaluerCoupLigne(plateau: list, indiceLigne: int, indiceColonne: int, couleurPion: int) -> int:
    """
    Evalue, pour la case donnée, le nombre de lignes encore complétables par couleurPion

    :param plateau: Plateau à analyser
    :param indiceLigne: Entier représentant l'indice de la ligne de la case étudiée
    :param indiceColonne: Entier représentant l'indice de la colonne de la case étudiée
    :param couleurPion: Couleur du pion pour lequel on fait l'évaluation
    :return: Entier représentant le nombre de possibilités
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le deuxième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du deuxième paramètre ne représente pas une ligne existante
    :raise TypeError: Si le troisième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du troisième paramètre ne représente pas une colonne existante
    :raise TypeError: Si le quatrième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du quatrième paramètre ne représente pas une couleur existante
    """
    if not type_plateau(plateau):
        raise TypeError("evaluerCoupLigne : Le premier paramètre ne correspond pas à un plateau.")
    if type(indiceLigne) is not int:
        raise TypeError("evaluerCoupLigne : Le deuxième paramètre ne correspond pas à un entier.")
    if indiceLigne < 0 or indiceLigne >= const.NB_LINES:
        raise ValueError("evaluerCoupLigne : Le deuxième paramètre n'est pas à un indice de ligne valide.")
    if type(indiceColonne) is not int:
        raise TypeError("evaluerCoupLigne : Le troisième paramètre ne correspond pas à un entier.")
    if indiceColonne < 0 or indiceColonne >= const.NB_COLUMNS:
        raise ValueError("evaluerCoupLigne : Le troisème paramètre n'est pas un indice de colonne valide.")
    if type(couleurPion) is not int:
        raise TypeError("evaluerCoupLigne : Le quatrième paramètre ne correspond pas à un entier.")
    if couleurPion not in const.COULEURS:
        raise ValueError("evaluerCoupLigne : Le quatrième paramètre ne correspond pas à une couleur.")
    nbPossibilites = 0
    # Pour chaque case débutant une ligne envisageable
    for colonne in range(const.NB_COLUMNS-3):
        # Si la case étudiée se trouve dans la ligne envisageable
        if (colonne <= indiceColonne) and (indiceColonne <= (colonne + 3)):
            # On évalue s'il est encore possible pour l'IA de la compléter
            possible = True
            i = 0
            while i < 4 and possible is True:
                if (plateau[indiceLigne][colonne + i] is not None
                   and plateau[indiceLigne][colonne + i][const.COULEUR] != couleurPion):
                    possible = False
                i += 1
            if possible:
                nbPossibilites += 1
    return nbPossibilites


def evaluerCoupColonne(plateau: list, indiceLigne: int, indiceColonne: int, couleurPion: int) -> int:
    """
    Evalue, pour la case donnée, le nombre de colonnes encore complétables par couleurPion

    :param plateau: Plateau à analyser
    :param indiceLigne: Entier représentant l'indice de la ligne de la case étudiée
    :param indiceColonne: Entier représentant l'indice de la colonne de la case étudiée
    :param couleurPion: Couleur du pion pour lequel on fait l'évaluation
    :return: Entier représentant le nombre de possibilités
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le deuxième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du deuxième paramètre ne représente pas une ligne existante
    :raise TypeError: Si le troisième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du troisième paramètre ne représente pas une colonne existante
    :raise TypeError: Si le quatrième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du quatrième paramètre ne représente pas une couleur existante
    """
    if not type_plateau(plateau):
        raise TypeError("evaluerCoupColonne : Le premier paramètre ne correspond pas à un plateau.")
    if type(indiceLigne) is not int:
        raise TypeError("evaluerCoupColonne : Le deuxième paramètre ne correspond pas à un entier.")
    if indiceLigne < 0 or indiceLigne >= const.NB_LINES:
        raise ValueError("evaluerCoupColonne : Le deuxième paramètre n'est pas un indice de ligne valide.")
    if type(indiceColonne) is not int:
        raise TypeError("evaluerCoupColonne : Le troisième paramètre ne correspond pas à un entier.")
    if indiceColonne < 0 or indiceColonne >= const.NB_COLUMNS:
        raise ValueError("evaluerCoupColonne : Le troisème paramètre n'est pas un indice de colonne valide.")
    if type(couleurPion) is not int:
        raise TypeError("evaluerCoupColonne : Le quatrième paramètre ne correspond pas à un entier.")
    if couleurPion not in const.COULEURS:
        raise ValueError("evaluerCoupColonne : Le quatrième paramètre ne correspond pas à une couleur.")
    nbPossibilites = 0
    # Pour chaque case débutant une colonne envisageable
    for ligne in range(const.NB_LINES-3):
        # Si la case étudiée se trouve dans la colonne envisageable
        if (ligne <= indiceLigne) and (indiceLigne <= (ligne + 3)):
            # On évalue s'il est encore possible pour l'IA de la compléter
            possible = True
            i = 0
            while i < 4 and possible is True:
                if (plateau[ligne + i][indiceColonne] is not None
                   and plateau[ligne + i][indiceColonne][const.COULEUR] != couleurPion):
                    possible = False
                i += 1
            if possible:
                nbPossibilites += 1
    return nbPossibilites


def evaluerCoupDiagonaleDirecte(plateau: list, indiceLigne: int, indiceColonne: int, couleurPion: int) -> int:
    """
    Evalue, pour la case donnée, le nombre de diagonales encore complétables par couleurPion

    :param plateau: Plateau à analyser
    :param indiceLigne: Entier représentant l'indice de la ligne de la case étudiée
    :param indiceColonne: Entier représentant l'indice de la colonne de la case étudiée
    :param couleurPion: Couleur du pion pour lequel on fait l'évaluation
    :return: Entier représentant le nombre de possibilités
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le deuxième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du deuxième paramètre ne représente pas une ligne existante
    :raise TypeError: Si le troisième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du troisième paramètre ne représente pas une colonne existante
    :raise TypeError: Si le quatrième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du quatrième paramètre ne représente pas une couleur existante
    """
    if not type_plateau(plateau):
        raise TypeError("evaluerCoupDiagonaleDirecte : Le premier paramètre ne correspond pas à un plateau.")
    if type(indiceLigne) is not int:
        raise TypeError("evaluerCoupDiagonaleDirecte : Le deuxième paramètre ne correspond pas à un entier.")
    if indiceLigne < 0 or indiceLigne >= const.NB_LINES:
        raise ValueError("evaluerCoupDiagonaleDirecte : Le deuxième paramètre n'est pas un indice de ligne valide.")
    if type(indiceColonne) is not int:
        raise TypeError("evaluerCoupDiagonaleDirecte : Le troisième paramètre ne correspond pas à un entier.")
    if indiceColonne < 0 or indiceColonne >= const.NB_COLUMNS:
        raise ValueError("evaluerCoupDiagonaleDirecte : Le troisème paramètre n'est pas un indice de colonne valide.")
    if type(couleurPion) is not int:
        raise TypeError("evaluerCoupDiagonaleDirecte : Le quatrième paramètre ne correspond pas à un entier.")
    if couleurPion not in const.COULEURS:
        raise ValueError("evaluerCoupDiagonaleDirecte : Le quatrième paramètre ne correspond pas à une couleur.")
    nbPossibilites = 0
    # Pour chaque case débutant une diagonale envisageable
    for ligne in range(const.NB_LINES-3):
        for colonne in range(const.NB_COLUMNS-3):
            # Si la case étudiée se trouve dans la diagonale envisageable
            if (indiceLigne, indiceColonne) in ((ligne, colonne), (ligne + 1, colonne + 1),
                                                (ligne + 2, colonne + 2), (ligne + 3, colonne + 3)):
                # On évalue s'il est encore possible pour l'IA de la compléter
                possible = True
                i = 0
                while i < 4:
                    if (plateau[ligne + i][colonne + i] is not None
                       and plateau[ligne + i][colonne + i][const.COULEUR] != couleurPion):
                        possible = False
                    i += 1
                if possible:
                    nbPossibilites += 1
    return nbPossibilites


def evaluerCoupDiagonaleIndirecte(plateau: list, indiceLigne: int, indiceColonne: int, couleurPion: int) -> int:
    """
    Evalue, pour la case donnée, le nombre d'anti-diagonales encore complétables par couleurPion

    :param plateau: Plateau à analyser
    :param indiceLigne: Entier représentant l'indice de la ligne de la case étudiée
    :param indiceColonne: Entier représentant l'indice de la colonne de la case étudiée
    :param couleurPion: Couleur du pion pour lequel on fait l'évaluation
    :return: Entier représentant le nombre de possibilités
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le deuxième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du deuxième paramètre ne représente pas une ligne existante
    :raise TypeError: Si le troisième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du troisième paramètre ne représente pas une colonne existante
    :raise TypeError: Si le quatrième paramètre n'est pas un entier
    :raise ValueError: Si l'entier du quatrième paramètre ne représente pas une couleur existante
    """
    if not type_plateau(plateau):
        raise TypeError("evaluerCoupDiagonaleIndirecte : Le premier paramètre ne correspond pas à un plateau.")
    if type(indiceLigne) is not int:
        raise TypeError("evaluerCoupDiagonaleIndirecte : Le deuxième paramètre ne correspond pas à un entier.")
    if indiceLigne < 0 or indiceLigne >= const.NB_LINES:
        raise ValueError("evaluerCoupDiagonaleIndirecte : Le deuxième paramètre n'est pas un indice de ligne valide.")
    if type(indiceColonne) is not int:
        raise TypeError("evaluerCoupDiagonaleIndirecte : Le troisième paramètre ne correspond pas à un entier.")
    if indiceColonne < 0 or indiceColonne >= const.NB_COLUMNS:
        raise ValueError("evaluerCoupDiagonaleIndirecte : Le troisème paramètre n'est pas un indice de colonne valide.")
    if type(couleurPion) is not int:
        raise TypeError("evaluerCoupDiagonaleIndirecte : Le quatrième paramètre ne correspond pas à un entier.")
    if couleurPion not in const.COULEURS:
        raise ValueError("evaluerCoupDiagonaleIndirecte : Le quatrième paramètre ne correspond pas à une couleur.")
    nbPossibilites = 0
    # Pour chaque case débutant une anti-diagonale envisageable
    for ligne in range(const.NB_LINES - 3):
        for colonne in range(3, const.NB_COLUMNS):
            # Si la case étudiée se trouve dans la diagonale envisageable
            if (indiceLigne, indiceColonne) in ((ligne, colonne), (ligne+1, colonne-1),
                                                (ligne+2, colonne-2), (ligne+3, colonne-3)):
                # On évalue s'il est encore possible pour l'IA de la compléter
                possible = True
                i = 0
                while i < 4:
                    if (plateau[ligne + i][colonne - i] is not None
                       and plateau[ligne + i][colonne - i][const.COULEUR] != couleurPion):
                        possible = False
                    i += 1
                if possible:
                    nbPossibilites += 1
    return nbPossibilites


def evaluerCoup(plateau: list, couleurJoueur: int) -> int:
    """
    Evalue la valeur d'un coup pour le joueur donné

    :param plateau: Plateau à analyser
    :param joueur: Joueur pour lequel on fait l'évaluation
    :return: Entier représentant le nombre de possibilités
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    :raise TypeError: Si le deuxième paramètre n'est pas un entier
    :raise ValueError: SI l'entier n'est pas une couleur
    """
    if not type_plateau(plateau):
        raise TypeError("evaluerCoup : Le premier paramètre ne correspond pas à un plateau.")
    if type(couleurJoueur) is not int:
        raise TypeError("evaluerCoup : Le deuxième paramètre n'est pas un entier.")
    if couleurJoueur not in const.COULEURS:
        raise ValueError("evaluerCoup : Le deuxième paramètre n'est pas une couleur.")
    nbPossibilites = 0
    # Pour chaque couleur de pion possible, on parcourt chaque case du plateau
    for couleur in const.COULEURS:
        for ligne in range(const.NB_LINES):
            for colonne in range(const.NB_COLUMNS):
                # Si la couleur étudiée est celle du joueur étudiée, les évaluations sont bénéfiques pour le joueur
                if couleur == couleurJoueur:
                    nbPossibilites += evaluerCoupLigne(plateau, ligne, colonne, couleur)
                    nbPossibilites += evaluerCoupColonne(plateau, ligne, colonne, couleur)
                    nbPossibilites += evaluerCoupDiagonaleDirecte(plateau, ligne, colonne, couleur)
                    nbPossibilites += evaluerCoupDiagonaleIndirecte(plateau, ligne, colonne, couleur)
                # Sinon la couleur étudiée est celle de l'adversaire et les évaluations ne sont pas bénéfiques au joueur
                else:
                    nbPossibilites -= evaluerCoupLigne(plateau, ligne, colonne, couleur)
                    nbPossibilites -= evaluerCoupColonne(plateau, ligne, colonne, couleur)
                    nbPossibilites -= evaluerCoupDiagonaleDirecte(plateau, ligne, colonne, couleur)
                    nbPossibilites -= evaluerCoupDiagonaleIndirecte(plateau, ligne, colonne, couleur)
    return nbPossibilites


def minimax(plateau, profondeur, couleurJoueur, isIAJoueur):
    if profondeur == 0 or isRempliPlateau(plateau):
        return evaluerCoup(plateau, couleurJoueur)
    if isIAJoueur:
        valeur_max = float('-inf')
        for col in range(const.NB_COLUMNS):
            if plateau[0][col] is None:
                copiePlateau = copierPlateau(plateau)
                placerPionPlateau(copiePlateau, construirePion((couleurJoueur + 1) % 2), col)
                valeur_max = max(valeur_max, minimax(copiePlateau, profondeur - 1, (couleurJoueur + 1) % 2, False))
        return valeur_max
    else:
        valeur_min = float('inf')
        for col in range(const.NB_COLUMNS):
            if plateau[0][col] is None:
                copiePlateau = copierPlateau(plateau)
                placerPionPlateau(copiePlateau, construirePion((couleurJoueur + 1) % 2), col)
                valeur_min = min(valeur_min, minimax(copiePlateau, profondeur - 1, (couleurJoueur + 1) % 2, True))
        return valeur_min


def meilleurCoup(plateau, couleurJoueur):
    meilleur_score = float('-inf')
    meilleur_colonne = None
    for colonne in range(7):
        if plateau[0][colonne] is None:
            copiePlateau = copierPlateau(plateau)
            placerPionPlateau(copiePlateau, construirePion((couleurJoueur + 1) % 2), colonne)
            score = minimax(copiePlateau, 3, couleurJoueur, False)  # Profondeur de recherche (à ajuster selon les performances)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_colonne = colonne
    return meilleur_colonne
