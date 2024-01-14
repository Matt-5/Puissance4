from Model.Constantes import *
from Model.Plateau import *
from Model.Joueur import *
from random import randint


def copierPlateau(plateau: list) -> list:
    """
    Copie en profondeur un plateau

    :param plateau: Plateau à copier
    :return: Liste de liste correspondant à une copie profonde du plateau
    :raise TypeError: Si le premier paramètre n'est pas un plateau
    """
    if not type_plateau(plateau):
        raise TypeError("copierPlateau : Le premier paramètre ne correspond pas à un plateau.")
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


def trouverCoup(joueur: dict, plateau: list, couleurJoueur: int) -> int:
    """
    Choisit semi-aléatoirement le numéro de la ligne/colonne à jouer

    :param joueur: Joueur pour lequel on cherche l'endroit où placer le pion
    :param plateau: Plateau à analyser
    :param couleurJoueur: Couleur du joueur pour lequel on cherche l'endroit où placer le pion
    :return: Entier représentant le numéro de la ligne/colonne à jouer
    """
    colonneChoisie = -(const.NB_LINES+1)
    favorableIA = False
    # Défintion des bornes de début et de fin de la recherche
    if const.MODE_ETENDU not in joueur:
        colonne = 0
        fin = const.NB_COLUMNS
    else:
        colonne = -const.NB_LINES
        fin = const.NB_COLUMNS + const.NB_LINES
    # Tant que l'on a pas parcouru tous les coups possibles et que l'on a pas trouvé de coup permettant à l'IA de gagner
    while colonne < fin and not favorableIA:
        copiePlateau = copierPlateau(plateau)
        # On place un pion de la couleur du joueur dans la grille
        placerPionLigneEtOuColonne(copiePlateau, colonne, couleurJoueur)
        # Si on détecte la réalisation d'une combinaison gagnante pour le joueur, on choisit cette position
        if isFinPossible(copiePlateau, couleurJoueur):
            colonneChoisie = colonne
            favorableIA = True
        # Si ce cas n'est pas favorable à une victoire du joueur
        if colonneChoisie == -(const.NB_LINES+1):
            copiePlateau = copierPlateau(plateau)
            # On place un pion de la couleur du joueur adverse dans la grille
            placerPionLigneEtOuColonne(copiePlateau, colonne, (couleurJoueur + 1) % 2)
            # Si on détecte la réalisation d'une combinaison gagnante pour le joueur adverse, on choisit cette position
            if isFinPossible(copiePlateau, (couleurJoueur + 1) % 2):
                colonneChoisie = colonne
                favorableIA = False
        colonne += 1
    # Si l'on a pas trouvé de coup "intelligent" pour l'IA, on choisit aléatoirement où jouer
    if colonneChoisie == -(const.NB_LINES+1):
        if const.MODE_ETENDU not in joueur:
            colonneChoisie = randint(0, const.NB_COLUMNS - 1)
            while joueur[const.PLATEAU][0][colonneChoisie] is not None:
                colonneChoisie = randint(0, const.NB_COLUMNS - 1)
        else:
            colonneChoisie = randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES)
            while (((0 <= colonneChoisie) and (colonneChoisie < const.NB_COLUMNS))
                   and (joueur[const.PLATEAU][0][colonneChoisie] is not None)):
                colonneChoisie = randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES)
    return colonneChoisie


def isFinPossible(plateau: list, couleurJoueur: int) -> bool:
    """
    Détermine si le joueur de la couleur indiquée à gagner

    :param plateau: Plateau à analyser
    :param couleurJoueur: Couleur du joueur
    :return: True s'il a gagné, False sinon
    """
    return (len(detecter4horizontalPlateau(plateau, couleurJoueur)) != 0
            or len(detecter4verticalPlateau(plateau, couleurJoueur)) != 0
            or len(detecter4diagonaleDirectePlateau(plateau, couleurJoueur)) != 0
            or len(detecter4diagonaleIndirectePlateau(plateau, couleurJoueur)) != 0)


def placerPionLigneEtOuColonne(plateau: list, colonne: int, couleurJoueur) -> None:
    """
    Place un pion de la couleur indiquée dans la ligne/colonne indiquée

    :param plateau: Plateau à analyser
    :param colonne: Indice représentant une ligne ou une colonne
    :param couleurJoueur: Couleur du joueur pour lequel il faut placer un pion
    :return: Aucun
    """
    if (0 <= colonne and colonne < const.NB_COLUMNS) and plateau[0][colonne] is None:
        placerPionPlateau(plateau, construirePion(couleurJoueur), colonne)
    elif colonne < 0:
        placerPionLignePlateau(plateau, construirePion(couleurJoueur), abs(colonne) - 1, True)
    elif colonne >= const.NB_COLUMNS:
        placerPionLignePlateau(plateau, construirePion(couleurJoueur), colonne - (const.NB_LINES + 1), False)
    return None
