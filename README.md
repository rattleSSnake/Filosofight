# Filosofight

#### Projet 1 NSI - Terminale

(Selon Diego) : Jeu en un contre un où un ELEVE (Joueur 1 - WASD) affronte un PROF DE PHILO (Joueur 2 - Flèches directionnelles).
Le combat est effectué à la manière d'un bossfight, en d'autres termes, le prof de philo a des attaques plus puissantes mais se déplace plus lentement, et vice-versa pour l'élève.
L'écran est divisé horizontalement en deux parties, celle du haut étant celle du prof de philo, celle du bas de l'élève.

### PROF DE PHILO:

Attaques:

- Rayon laser (cooldown élevé) avec une texture représentant une citation écrite mot pour mot. (On choisira plusieurs citations et elles seront choisies aléatoirement par le programme au moment de lancer l'attaque, pour varier les affichages)
- Lancer de livres. (plusieurs textures de livres différentes, choisies aléatoirement lors de l'éxecution du programme)

### ELEVE:

Peut esquiver (??),
Attaques:

- Lance des crayons à papier à une fréquence élevée.
- Peut poser une table devant lui qui lui sert de bouclier temporaire. (La table possède un certain nombre de points de vie et disparaît quand elle n'en a plus)
- Lancer de livres. (pour recycler au moins une fonction)

## Classes nécessaires:

- Joueur
- Prof
- Table
- Livre
- Crayon
- CitationLaser
- -> Classe Main qui centralise l'éxécution générale du jeu??
