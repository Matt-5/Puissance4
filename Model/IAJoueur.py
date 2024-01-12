from Model.Constantes import *


def evaluerPosition(plateau: list, couleurPion: int) -> list:
    matricePossibilites = []
    for ligne in range(const.NB_LINES):
        nouvelleLigne = []
        for colonne in range(const.NB_COLUMNS):
            nouvelleLigne.append(evaluerPositionLigne(plateau, ligne, colonne, couleurPion)
                                 + evaluerPositionColonne(plateau, ligne, colonne, couleurPion)
                                 + evaluerPositionDiagonaleDirecte(plateau, ligne, colonne, couleurPion)
                                 + evaluerPositionDiagonaleIndirecte(plateau, ligne, colonne, couleurPion))
        matricePossibilites.append(nouvelleLigne)
    return matricePossibilites


def evaluerPositionLigne(plateau: list, indiceLigne: int, indiceColonne: int, couleurPion: int) -> int:
    nbPossibilites = 0
    for i in range(const.NB_COLUMNS-3):
        if (i <= indiceColonne) and (indiceColonne <= (i + 3)):
            possible = True
            for k in range(i, i+4):
                if plateau[indiceLigne][k] is not None and plateau[indiceLigne][k][const.COULEUR] != couleurPion:
                    possible = False
            if possible:
                nbPossibilites += 1
    return nbPossibilites


def evaluerPositionColonne(plateau: list, indiceLigne: int, indiceColonne: int, couleurPion: int) -> int:
    nbPossibilites = 0
    for i in range(const.NB_LINES-3):
        if (i <= indiceLigne) and (indiceLigne <= (i + 3)):
            possible = True
            for k in range(i, i+4):
                if plateau[k][indiceColonne] is not None and plateau[k][indiceColonne][const.COULEUR] != couleurPion:
                    possible = False
            if possible:
                nbPossibilites += 1
    return nbPossibilites


def evaluerPositionDiagonaleDirecte(plateau: list, indiceLigne: int, indiceColonne: int, couleurPion: int) -> int:
    nbPossibilites = 0
    couplesPossibles = []
    for i in range(const.NB_LINES-3):
        for j in range(const.NB_COLUMNS-3):
            possible = True
            for k in range(4):
                if plateau[i+k][j+k] is not None and plateau[i + k][j + k][const.COULEUR] != couleurPion:
                    possible = False
            if possible:
                couplesPossibles.append([(i, j), (i+1, j+1), (i+2, j+2), (i+3, j+3)])
    for diagonale in couplesPossibles:
        if (indiceLigne, indiceColonne) in diagonale:
            nbPossibilites += 1
    return nbPossibilites


def evaluerPositionDiagonaleIndirecte(plateau: list, indiceLigne: int, indiceColonne: int, couleurPion: int) -> int:
    nbPossibilites = 0
    couplesPossibles = []
    for i in range(const.NB_LINES - 3):
        for j in range(3, const.NB_COLUMNS):
            possible = True
            for k in range(0, 4):
                if plateau[i + k][j - k] is not None and plateau[i + k][j - k][const.COULEUR] != couleurPion:
                    possible = False
            if possible:
                couplesPossibles.append([(i, j), (i+1, j-1), (i+2, j-2), (i+3, j-3)])
    for diagonale in couplesPossibles:
        if (indiceLigne, indiceColonne) in diagonale:
            nbPossibilites += 1
    return nbPossibilites
