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


def trouverCoup(joueur: dict) -> int:
    colonneChoisie = -1
    favorableIA = False
    if const.MODE_ETENDU not in joueur:
        colonne = 0
        while colonne < const.NB_COLUMNS and not favorableIA:
            if joueur[const.PLATEAU][0][colonne] is None:
                plateau = getPlateauJoueur(joueur)
                copiePlateau = copierPlateau(plateau)
                placerPionPlateau(copierPlateau, construirePion(getCouleurJoueur(joueur)), colonne)
                # Si on détecte la réalisation d'une combinaise gagnante pour le joueur, on choisit cette position
                if (len(detecter4horizontalPlateau(copiePlateau), getCouleurJoueur(joueur)) != 0
                    or len(detecter4verticalPlateau(copiePlateau), getCouleurJoueur(joueur)) != 0
                    or len(detecter4diagonaleDirectePlateau(copiePlateau), getCouleurJoueur(joueur)) != 0
                    or len(detecter4diagonaleIndirectePlateau(copiePlateau), getCouleurJoueur(joueur)) != 0):
                    colonneChoisie = colonne
                    favorableIA = True
                elif (len(detecter4horizontalPlateau(copiePlateau), (getCouleurJoueur(joueur)+1)%2) != 0
                      or len(detecter4verticalPlateau(copiePlateau), (getCouleurJoueur(joueur)+1)%2) != 0
                      or len(detecter4diagonaleDirectePlateau(copiePlateau), (getCouleurJoueur(joueur)+1)%2) != 0
                      or len(detecter4diagonaleIndirectePlateau(copiePlateau), (getCouleurJoueur(joueur)+1)%2) != 0):
                    colonneChoisie = colonne
            colonne += 1
        if colonneChoisie == -1:
            colonneChoisie = randint(0, const.NB_COLUMNS - 1)
            while joueur[const.PLATEAU][0][colonneChoisie] is not None:
                colonneChoisie = randint(0, const.NB_COLUMNS - 1)
    return colonneChoisie
