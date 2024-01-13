from Model.Constantes import *
from Model.Pion import *
from Model.Plateau import *
from random import randint


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
    if type(joueur) is not dict:
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


def construireJoueur(couleur: int) -> dict:
    """
    Permet de construire un joueur

    :param couleur: Couleur du joueur à construire
    :return: Dictionnaire représentant un joueur
    :raise TypeError: Si le paramètre n'est pas un entier
    :raise ValueError: Si l'entier ne représente pas une couleur
    """
    if type(couleur) is not int:
        raise TypeError("construireJoueur : Le paramètre n’est pas un entier.")
    if couleur not in const.COULEURS:
        raise ValueError(f"construireJoueur : L'entier donné {couleur} n'est pas une couleur.")
    return {const.COULEUR: couleur, const.PLATEAU: None, const.PLACER_PION: None}


def getCouleurJoueur(joueur: dict) -> int:
    """
    Récupère la couleur d'un joueur

    :param joueur: Joueur dont il faut récupérer la couleur
    :return: Entier représentant la couleur du joueur
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getCouleurJoueur : Le paramètre ne correspond pas à un joueur.")
    return joueur[const.COULEUR]


def getPlateauJoueur(joueur: dict) -> list:
    """
    Récupère le plateau d'un joueur

    :param joueur: Joueur dont il faut récupérer le plateau
    :return: Liste de listes correspondant au plateau
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getPlateauJoueur : Le paramètre ne correspond pas à un joueur.")
    return joueur[const.PLATEAU]


def getPlacerPionJoueur(joueur: dict) -> callable:
    """
    Récupère la fonction contenue dans le dictionnaire du joueur

    :param joueur: Joueur dont il faut récupérer la fonction
    :return: La fonction récupérée
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getPlacerPionJoueur : Le paramètre ne correspond pas à un joueur.")
    return joueur[const.PLACER_PION]


def getPionJoueur(joueur: dict) -> dict:
    """
    Construit un pion utilisant la couleur du joueur passé en paramètre

    :param joueur: Joueur dont il faut récupérer la couleur
    :return: Dictionnaire représentant un pion créé avec la couleur du joueur
    :raise TypeError: Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getPionJoueur : Le paramètre ne correspond pas à un joueur.")
    return construirePion(getCouleurJoueur(joueur))


def setPlateauJoueur(joueur: dict, plateau: list) -> None:
    """
    Affecte un plateau à un joueur

    :param joueur: Joueur auquel il faut affecter le plateau
    :param plateau: Plateau à affecter au joueur
    :return: Aucun
    :raise TypeError: Si le premier paramètre n'est pas un joueur
    :raise TypeError: Si le second paramètre n'est pas un plateau
    """
    if not type_joueur(joueur):
        raise TypeError("setPlateauJoueur : Le premier paramètre ne correspond pas à un joueur.")
    if not type_plateau(plateau):
        raise TypeError("setPlateauJoueur : Le second paramètre ne correspond pas à un plateau.")
    joueur[const.PLATEAU] = plateau
    return None


def setPlacerPionJoueur(joueur: dict, fonction: callable) -> None:
    """
    Affecte une fonction à un joueur

    :param joueur: Joueur auquel il faut affecter la fonction
    :param fonction: Fonction à affecter au joueur
    :return: Aucun
    :raise TypeError: Si le premier paramètre n'est pas un joueur
    :raise TypeError: Si le second paramètre n'est pas une fonction
    """
    if not type_joueur(joueur):
        raise TypeError("setPlacerPionJoueur : Le premier paramètre ne correspond pas à un joueur.")
    if not callable(fonction):
        raise TypeError("setPlacerPionJoueur : Le second paramètre n'est pas une fonction.")
    joueur[const.PLACER_PION] = fonction
    return None


def _placerPionJoueur(joueur: dict) -> int:
    """
    Choisit aléatoirement le numéro de la colonne à jouer

    :param joueur: Joueur (IA) pour lequel il faut choisir la colonne à jouer
    :return: Aucun
    """
    # Si l'on est pas en mode étendu
    if const.MODE_ETENDU not in joueur:
        nbAlea = randint(0, const.NB_COLUMNS - 1)
        while joueur[const.PLATEAU][0][nbAlea] is not None:
            nbAlea = randint(0, const.NB_COLUMNS - 1)
    # Sinon, on est en mode étendu
    else:
        nbAlea = randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES - 1)
        while ((0 <= nbAlea) and (nbAlea < const.NB_COLUMNS)) and (joueur[const.PLATEAU][0][nbAlea] is not None):
            nbAlea = randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES - 1)
    return nbAlea


def initialiserIAJoueur(joueur: dict, premier: bool) -> None:
    """
    Affectela fonction _placerPionJoueur au joueur (IA)

    :param joueur: Joueur (IA) à initialiser
    :param premier: Booléen définissant si le joueur joue en premier (True) ou en second (False)
    :return: Aucun
    :raise TypeError: Si le premier paramètre n'est pas un joueur
    :raise TypeError: Si le second paramètre n'est pas un booléen
    """
    if not type_joueur(joueur):
        raise TypeError("initialiserIAJoueur : Le premier paramètre ne correspond pas à un joueur.")
    if type(premier) is not bool:
        raise TypeError("initialiserIAJoueur : Le second paramètre n'est pas un booléen.")
    setPlacerPionJoueur(joueur, _placerPionJoueur)
    return None


def getModeEtenduJoueur(joueur: dict) -> bool:
    """
    Evalue si un joueur est en mode étendu
    :param joueur: Joueur à évaluer
    :return: True si le mode étendu est actif, False sinon
    :raise TypeError : Si le paramètre n'est pas un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getModeEtenduJoueur : Le paramètre ne correspond pas à un joueur.")
    if const.MODE_ETENDU in joueur:
        retour = True
    else:
        retour = False
    return retour


def setModeEtenduJoueur(joueur: dict, modeEtendu: bool = True) -> None:
    """
    Modifie un joueur en fonction de sa présence ou non en mode étendu

    :param joueur: Joueur à modifier
    :param modeEtendu: Booléen définissant si on doit ajouter ou supprimer la clé const.MODE_ETENDU
    :return: Aucun
    :raise TypeError : Si le premier paramètre n'est pas un joueur
    :raise TypeError : Si le second paramètre n'est pas un booléen
    """
    if not type_joueur(joueur):
        raise TypeError("setModeEtenduJoueur : Le premier paramètre ne correspond pas à un joueur.")
    if type(modeEtendu) is not bool:
        raise TypeError("setModeEtenduJoueur : Le second paramètre ne correspond pas à un booléen.")
    # Si on doit désactiver le mode étendu
    if not modeEtendu:
        # On désactive le mode étendu seulement si il n'était pas déjà désactivé
        if const.MODE_ETENDU in joueur:
            del joueur[const.MODE_ETENDU]
    # Sinon, il faut l'activer
    else:
        joueur[const.MODE_ETENDU] = True
    return None
