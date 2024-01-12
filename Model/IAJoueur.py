from Model.Constantes import *

def evaluerPosition(plateau:list)->list:
    matricePossibilites = []
    for ligne in range(const.NB_LINES):
        nouvelleLigne = []
        for colonne in range (const.NB_COLUMNS):
            nouvelleLigne.append(evaluerPositionDiagonaleDirecte(ligne, colonne, 1))
        matricePossibilites.append(nouvelleLigne)
    return matricePossibilites


def evaluerPositionLigne(indiceLigne:int, indiceColonne:int, couleurPion:int)->int:
    nbPossibilites = 0
    for i in range(const.NB_COLUMNS-3):
        if i <= indiceColonne and indiceColonne <= (i + 3):
            possible = True
            for k in range(i, i+4):
                if plateau[indiceLigne][k] == None or plateau[indiceLigne][k] != couleurPion:
                    possible = False
            if possible:
                nbPossibilites += 1
    return nbPossibilites


def evaluerPositionColonne(indiceLigne:int, indiceColonne:int, couleurPion:int)->int:
    nbPossibilites = 0
    for i in range(const.NB_LINES-3):
        if i <= indiceLigne and indiceLigne <= (i + 3):
            possible = True
            for k in range(i, i+4):
                if plateau[k][indiceColonne] == None or plateau[k][indiceColonne] != couleurPion:
                    possible = False
            if possible:
                nbPossibilites += 1
    return nbPossibilites


def evaluerPositionDiagonaleDirecte(indiceLigne:int, indiceColonne:int, couleurPion:int)->int:
    nbPossibilites = 0
    for i in range(const.NB_LINES-4):
        for j in range(const.NB_COLUMNS-4):
            if (i <= indiceLigne and indiceLigne <= (min(i + 3, const.NB_LINES))) and (j <= indiceColonne and indiceColonne <= (min(j + 3, const.NB_COLUMNS))):
                possible = True
                for k in range(i, i+4):
                    if plateau[i + k][j + k] == None or plateau[i + k][i + k] != couleurPion:
                        possible = False
                if possible:
                    nbPossibilites += 1
    return nbPossibilites


def evaluerPositionDiagonaleIndirecte(indiceLigne:int, indiceColonne:int, couleurPion:int)->int:
    nbPossibilites = 0
    for i in range(const.NB_LINES-4):
        for j in range(3, const.NB_COLUMNS):
            if (i <= indiceLigne and indiceLigne <= (i + 3)) and (j <= indiceColonne and indiceColonne <= (j + 3)):
                possible = True
                for k in range(i, i+4):
                    if plateau[i + k][j - k] == None or plateau[i + k][i - k] != couleurPion:
                        possible = False
                if possible:
                    nbPossibilites += 1
    return nbPossibilites

plateau= [[1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1]]
print(evaluerPosition(plateau))