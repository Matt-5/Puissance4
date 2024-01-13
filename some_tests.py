from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from random import randint, choice

p = construirePlateau()
print(p)
pion = construirePion(const.JAUNE)
line = placerPionPlateau(p, pion, 2)
print("Placement d’un pion en colonne 2. Numéro de ligne :", line)
print(p)

# Essais sur les couleurs
print("\x1B[43m \x1B[0m : carré jaune ")
print("\x1B[41m \x1B[0m : carré rouge ")
print("\x1B[41mA\x1B[0m : A sur fond rouge")

# Construction d'un plateau test composé de 30 pions de couleurs aléatoires
p = construirePlateau()
for _ in range(30):
    placerPionPlateau(p, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))

# Conversion du plateau en chaîne de caractères afin de pouvoir tester les fonctions visuellement
print(toStringPlateau(p))
# Tests des différentes fonctions de détection de 4 pions alignés pour une couleur définie
print(detecter4horizontalPlateau(p, const.ROUGE))
print(detecter4verticalPlateau(p, const.ROUGE))
print(detecter4diagonaleDirectePlateau(p, const.ROUGE))
print(detecter4diagonaleIndirectePlateau(p, const.ROUGE))
# Test de la fonction permettant d'obtenir tous les pions alignés du plateau, peu importe la couleur
print(getPionsGagnantsPlateau(p))
