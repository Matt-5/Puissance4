# Model/Pion.py

from Model.Constantes import *

#
# Ce fichier implémente les données/fonctions concernant le pion
# dans le jeu du Puissance 4
#
# Un pion est caractérisé par :
# - sa couleur (const.ROUGE ou const.JAUNE)
# - un identifiant de type int (pour l'interface graphique)
#
# L'identifiant sera initialisé par défaut à None
#


def type_pion(pion: dict) -> bool:
    """
    Détermine si le paramètre peut être ou non un Pion

    :param pion: Paramètre dont on veut savoir si c'est un Pion ou non
    :return: True si le paramètre correspond à un Pion, False sinon.
    """
    return type(pion) is dict and len(pion) == 2 and const.COULEUR in pion.keys() \
        and const.ID in pion.keys() \
        and pion[const.COULEUR] in const.COULEURS \
        and (pion[const.ID] is None or type(pion[const.ID]) is int)


def construirePion(couleur: int) -> dict:
    """
    Fonction permettant de construire un pion

    :param couleur: Couleur du pion à construire
    :return: Dictionnaire représentant un pion
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if type(couleur) is not int:
        raise TypeError("construirePion : Le paramètre n'est pas de type entier.")
    if couleur not in const.COULEURS:
        raise ValueError(f"construirePion : La couleur {couleur} n'est pas correcte.")
    return {const.COULEUR: couleur, const.ID: None}


def getCouleurPion(pion: dict) -> int:
    """
    Récupère la couleur d'un pion

    :param pion: Pion dont il faut récupérer la couleur
    :return: Entier représentant la couleur du pion
    :raise TypeError: Si le paramètre n'est pas un pion
    """
    if not type_pion(pion):
        raise TypeError("getCouleurPion : Le paramètre n'est pas un pion.")
    return pion[const.COULEUR]


def setCouleurPion(pion: dict, couleur: int) -> None:
    """
    Modifie la couleur d'un pion

    :param pion: Pion dont il faut modifier la couleur
    :param couleur: Couleur à affecter
    :return: Aucun
    :raise TypeError: Si le premier paramètre n'est pas un pion
    :raise TypeError: Si le second paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if not type_pion(pion):
        raise TypeError("setCouleurPion : Le premier paramètre n'est pas un pion.")
    if type(couleur) is not int:
        raise TypeError("setCouleurPion : Le second paramètre n'est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError(f"setCouleurPion : Le second paramètre {couleur} n'est pas une couleur.")
    pion[const.COULEUR] = couleur
    return None


def getIdPion(pion: dict) -> int:
    """
    Récupère l'identifiant d'un pion

    :param pion: Pion dont il faut récupérer l'identifiant
    :return: Entier représentant l'identifiant du pion
    :raise TypeError: Si le paramètre n'est pas un pion
    """
    if not type_pion(pion):
        raise TypeError("getIdPion : Le paramètre n'est pas un pion.")
    return pion[const.ID]


def setIdPion(pion: dict, valeur: int) -> None:
    """
    Modifier l'identifiant d'un pion

    :param pion: Pion dont il faut modifier l'identifiant
    :param valeur: Identifiant à affecter
    :return: Aucun
    :raise TypeError: Si le premier paramètre n'est pas un pion
    :raise TypeError: Si le second paramètre n'est pas un entier
    """
    if not type_pion(pion):
        raise TypeError("setIdPion : Le premier paramètre n'est pas un pion.")
    if type(valeur) is not int:
        raise TypeError("setIdPion : Le second paramètre n'est pas un entier.")
    pion[const.ID] = valeur
    return None
