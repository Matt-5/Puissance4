from Model.Constantes import *
from Model.Pion import *
from Model.Plateau import *



#
# Ce fichier contient les fonctions gérant le joueur
#
# Un joueur sera un dictionnaire avec comme clé :
# - const.COULEUR : la couleur du joueur entre const.ROUGE et const.JAUNE
# - const.PLACER_PION : la fonction lui permettant de placer un pion, None par défaut,
#                       signifiant que le placement passe par l'interface graphique.
# - const.PLATEAU : référence sur le plateau de jeu, nécessaire pour l'IA, None par défaut
# - d'autres constantes nécessaires pour lui permettre de jouer à ajouter par la suite...
#

def type_joueur(joueur: dict) -> bool:
    """
    Détermine si le paramètre peut correspondre à un joueur.

    :param joueur: Paramètre à tester
    :return: True s'il peut correspondre à un joueur, False sinon.
    """
    if type(joueur) != dict:
        return False
    if const.COULEUR not in joueur or joueur[const.COULEUR] not in const.COULEURS:
        return False
    if const.PLACER_PION not in joueur or (joueur[const.PLACER_PION] is not None
            and not callable(joueur[const.PLACER_PION])):
        return False
    if const.PLATEAU not in joueur or (joueur[const.PLATEAU] is not None and
        not type_plateau(joueur[const.PLATEAU])):
        return False
    return True


def construireJoueur(couleur:int)-> dict:
    """
    Fonction permettant de construire un joueur
    :param couleur: Couleur du joueur à construire
    :return: Dictionnaire représentant un joueur
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if type(couleur) != int:
        raise TypeError("construireJoueur : Le paramètre n’est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError(f"construireJoueur : L'entier donné {couleur} n'est pas une couleur.")
    return {const.COULEUR : couleur, const.PLATEAU : None, const.PLACER_PION : None}


def getCouleurJoueur(joueur : dict)-> int:
    """
    Récupérer la couleur d'un joueur
    :param joueur: Joueur dont il faut récupérer la couleur
    :return: Un entier représentant la couleur du joueur
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if type_joueur(joueur) == False:
        raise TypeError("getCouleurJoueur : Le paramètre ne correspond pas à un joueur.")
    return joueur[const.COULEUR]


def getPlateauJoueur(joueur : dict)->list:
    """
    Récupérer le plateau d'un joueur
    :param joueur: Le joueur dont il faut récupérer le plateau
    :return: Une liste correspondant au plateau
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if type_joueur(joueur) == False:
        raise TypeError("getPlateauJoueur : Le paramètre ne correspond pas à un joueur.")
    return joueur[const.PLATEAU]


def getPlacerPionJoueur(joueur : dict)-> callable:
    """
    Récupérer la fonction contenue dans le dictionnaire d'un joueur
    :param joueur: Le joueur dont il faut récupérer la fonction
    :return: La fonction récupérée
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if type_joueur(joueur) == False:
        raise TypeError("getPlacerPionJoueur : Le paramètre ne correspond pas à un joueur.")
    return joueur[const.PLACER_PION]


def getPionJoueur(joueur : dict) -> dict:
    """
    Construire un pion utilisant la couleur du joueur donné en paramètre.
    :param joueur: Le joueur dont il faut récupérer la couleur
    :return: Le pion créé avec la couleur du joueur
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if type_joueur(joueur) == False:
        raise TypeError("getPionJoueur : Le paramètre ne correspond pas à un joueur.")
    return construirePion(getCouleurJoueur(joueur))


def setPlateauJoueur(joueur : dict, plateau : list)-> None:
    """
    Affecter un plateau à un joueur
    :param joueur: Le joueur auquel il faut affecter le plateau
    :param plateau: Le plateau à affecter au joueur
    :return: Aucun
    :raise TypeError: Si le paramètre n'est pas un joueur
    :raise TypeError: Si le paramètre n'est pas un plateau
    """
    if type_joueur(joueur) == False:
        raise TypeError("setPlateauJoueur : Le premier paramètre ne correspond pas à un joueur.")
    if type_plateau(plateau) == False:
        raise TypeError("setPlateauJoueur : Le second paramètre ne correspond pas à un plateau.")
    joueur[const.PLATEAU] = plateau
    return None


def setPlacerPionJoueur(joueur : dict, fonction : callable)-> None:
    """
    Affecter une fonction à un joueur
    :param joueur: Le joueur auquel il faut affecter la fonction
    :param fonction: La fonction à affecter au joueur
    :return: AUcun
    :raise TypeError: Si le paramètre n'est pas un joueur
    :raise TypeError: Si le paramètre n'est pas une fonction
    """
    if type_joueur(joueur) == False:
        raise TypeError("setPlacerPionJoueur : Le premier paramètre ne correspond pas à un joueur.")
    if callable(fonction) != True:
        raise TypeError("setPlacerPionJoueur : Le second paramètre n'est pas une fonction.")
    joueur[const.PLACER_PION] = fonction
    return None