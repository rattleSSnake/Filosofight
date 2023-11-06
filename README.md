# Filosofight

#### Projet 1 NSI - Terminale

Jeu en un contre un où un __ELEVE__ (Joueur 1 - Flèches directionnelles) affronte un __PROF DE PHILO__ (Joueur 2 - ZQSD).
Le combat est effectué à la manière d'un bossfight, en d'autres termes, le prof de philo est plus puissant mais plus lent que l'élève.
L'écran est divisé horizontalement en deux parties, celle du haut étant celle du prof de philo, celle du bas de l'élève.
Il y a un timer de 2 minutes 30, au bout duquel le Prof gagne si l'élève n'a pas réussi à vaincre le Prof (cela incite le joueur à être agressif et de prendre des risques car son principal avantage est de jouer une stratégie défensive, cas où il gagnerait presque à chaque fois s'il n'y avait pas de timer.)

### PROF DE PHILO:

- __Rayon laser__ (touche G) avec une texture représentant une citation écrite mot pour mot. Il y en a plusieurs et elles sont choisies aléatoirement par le programme. Elles ne sont malheureusement pas totalement visibles lors de l'exécution du programme du à la rapidité du défilement. Lorsque l'attaque est lancée, un rayon violet inoffensif se déclenche pour que l'Élève ait le temps d'esquiver. Quand le rayon devient rouge, il devient dangereux et inflige 50 dégâts à l'Élève. Cooldown de plusieurs secondes.
- __Lancer de crayons__ (touche F). Lancers à vitesse lente et cadence de tir plutôt lente. Inflige 10 dégâts.

### ELEVE:

- __Lancer de crayons__ (touche M). Lancers à vitesse plus rapide et cadence de tir rapide. Inflige 20 dégâts car l'Élève utilise un pistolet à crayons.
- Peut __poser une table__ devant lui (touche L) qui lui sert de bouclier temporaire. La table peut absorber 3 attaques de crayon, ou une citation et demie avant de se casser. Cooldown de plusieurs secondes. L'élève ne peut avoir que trois table sur l'écran en même temps.

## Classes utilisées:

- __Eleve__ (Joueur 1)
- __Prof__ (Joueur 2)
- __Table__ (Attaque)
- __Crayon__ (Attaque)
- __CitationLaser__ (Attaque)
- __AllSounds__ (Sound Management)
- __Main__ (Jeu principal)

## Méthodes:

__NOTE:__ Presque toutes les classes possèdent des méthodes dont l'utilité est la même. En outre, utiliser l'héritage de classe aurait été utile. Dû à un manque de temps il n'a pas été possible pour nous de transformer tout le programme, donc il existe des fonctions similaires un peu partout.
__NOTE 2:__ Il n'y a pas de documentation pour les __Getters__, les __Setters__ et les __ __init__ __() dans le programme, afin d'économiser du temps.

##### Méthodes communes à tout sprite

    def movement(self, dt: float, screen:pygame.Surface):
        """
        Permet de faire changer les coordonnées de l'instance de la classe, basé sur les commandes du clavier ou son comportement.\n
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement, 
        screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        ...
    
    def draw(self, screen:pygame.Surface):
        """
        Permet de dessiner à l'écran l'image de l'instance de la classe.\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        ...

##### Méthodes générales pour joueurs

    def affiche_hud(self, screen:pygame.Surface):
        """
        Permet d'afficher le HUD (affichage tête-haute).\n
        Paramètre:screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        ...

    def est_mort(self):
        """
        Permet de détecter quand la vie de l'instance de la classe est inférieure ou égale à 0.\n
        Renvoie: tuple avec True et l'instance de la classe.
        """
        ...

    def invincibilite(self):
        """
        Permet d'afficher une animation de clignotement pendant un temps donné sur le personnage à chaque fois qu'il est touché par une attaque. Fait usage de la fonction SINUS.
        """
        ...

##### Attaques

    def lance_crayon(self):
        """
        Permet de lancer l'attaque 'crayon', en créant une nouvelle instance de Crayon à la liste des attaques courantes.
        """
        ...

    def lance_citation(self):
        """
        Permet de lancer l'attaque 'citation', en créant une nouvelle instance de CitationLaser à la liste des attaques courantes.
        """
        ...

    def lance_table(self):
        """
        Permet de lancer l'attaque 'table', en créant une nouvelle instance de Table à la liste des attaques courantes.\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        ...

    def attack_management(self):
        """
        Procédure permettant de gérer en continu les pressions de touches, qui activeront chacune des attaques respectives (élève et prof).
        """
        ...

    def supprimer_dechets(self, table_list:list, index:int):
        """
        Supprime l'instance de la classe si elle complète les critères nécessaires.\n
        Paramètres:\n
        - table_list: liste contenant des instances de la classe Table. _n
        - index: nombre entier entre 0 et len(table_list).
        """
        ...

    def collisions(self, player, table_list:list[Table]):
        """
        Prend en charge les collisions entre cette instance du crayon et toutes les instances de la classe Table ainsi que
        de la classe Joueur encores présentes sur l'écran.\n
        Paramètres:\n
        - eleve: instance de la classe Eleve ou Prof.\n
        - table_list: liste contenant des instances de la classe Table, ou liste vide.
        """
        ...

    def retrecir(self, temps_soutrait: int, duree_fonction: int):
        """
        Cette fonction permet de rétrecir les dimensions du rectangle et de la texture jusqu'à faire quasi disparaître
        l'instance de la classe de l'écran, à l'aide d'une fonction ease-out circulaire.\n
        Paramètres:\n
        - temps_soustrait (int) -> Le temps à soustraire depuis l'apparition de l'instance de la classe jusqu'à l'instant présent
        afin que la variable x de la fonction ease-out commence de préférence à 0.\n
        - duree_fonction (int) -> Durée (en millisecondes) que devrait prendre en charge la fonction f.\n
        Pré-conditions:\n
        - temps_soustrait doît être de type int.\n
        - duree_fonction doît être de type int, strictement supérieure à 0.\n
        Renvoie: True si le rétrecissement peut encore continuer, False si l'image de f(x) est égale à 0.
        """
        ...

##### Sons

    def play_sfx(self, son: str, channel_id: int):
        """
        Joue un son parmi ceux qui existent dans cette classe.\n
        Paramètre: son (str), nom du sound_effect qui sera joué, channel_id (int) entre 1 et 7 qui va définir le channel sur lequel le son va être joué.
        """
        ...

##### Classe Main

    def is_game_over(self):
        """
        Fonction qui renvoie True ou False si l'un des joueurs meurt. Dans le cas où la fonction renvoie True, elle change
        aussi la valeur de gagnant pour indiquer le nom du gagnant.
        """
        ...

    def restart_manager(self):
        """
        Quand elle est appelée, cette méthode attend l'appui de la touche R pour réinitialiser le jeu à zéro.
        """
        ...

    def timer(self):
        """
        Prend en charge le calcul du temps et l'affichage du temps sur l'affichage tête haute.
        """
        ...

    def game(self):
        """
        Déroulement du jeu dans toute son intégralité. (boucle while)
        """
        ...

## Crédits

Thomas, Vincent, Diego
NSI Terminale, 2023