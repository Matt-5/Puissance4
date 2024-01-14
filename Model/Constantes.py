import const

# Constantes concernant la couleur des jetons ou des deux joueurs
const.ROUGE = 1
const.JAUNE = 0
const.COULEURS = [const.JAUNE, const.ROUGE]

# "Attributs" de Pion
const.COULEUR = "Couleur"
const.ID = "Identifiant"

# "Attributs" du joueur
const.PLACER_PION = "PlacerPion"
const.JEU_ADVERSAIRE = "JeuAdversaire"
const.PLATEAU = "Plateau"
const.MODE_ETENDU = "ModeEtendu"


# Dimensions du plateau
const.NB_LINES = 6
const.NB_COLUMNS = 7

# Niveau de l'IA
# 1 : IA "stupide" plaçant aléatoirement les pions
# 2 : IA utilisant l'algorithme MiniMax pour placer les pions
# Si la valeur du niveau pas une valeur possible, le programme considère que l'on joue au niveau 1
const.NIVEAU_IA = 2

# Dans la cas de l'algorithme MiniMax :
# Profondeur de recherche (A ADAPTER EN FONCTION DES PERFORMANCES DE LA MACHINE SUR LEQUEL LE PROGRAMME TOURNE !)
const.PROFONDEUR = 4
