import pygame
import random
import math
import time


class Prof:
    def __init__(self, vie: int, pos: tuple[int], LONGUEUR: int, LARGEUR: int):
        assert type(vie) == int, "Une valeur entière est attendue pour la vie."
        assert type(pos) == tuple, "Un tuple de coordonnées est attendu."
        assert type(LONGUEUR) == int and type(LARGEUR) == int, "Des valeurs entières sont attendues pour la dimension."
        self.vie = vie
        self.player_pos = pygame.Vector2(pos[0], pos[1])
        path = pygame.image.load(
            f"./Assets/Textures/PROF_PIXEL_{random.randint(1,2)}.png"
        )
        self.texture = path
        self.texture = pygame.transform.scale(self.texture, (132, 132))
        self.LONGUEUR, self.LARGEUR = LONGUEUR, LARGEUR
        self.orientation = "RIGHT"
        self.type = "PROF"
        # Animation
        self.a_ete_touche = False
        self.temps_invincible = 2000
        self.has_swapped_texture = False
        self.texture_hurt = pygame.image.load("./Assets/Textures/HURT.png")
        self.textures = [self.texture, self.texture_hurt]
        self.hurt_timer = 0
        # Crayon
        self.last_crayon = 0
        self.crayon_cadence_de_tir = 1100  # Millisecondes
        # Citations Lasers
        self.last_citation = 0
        self.citation_cadence_de_tir = 6000  # Millisecondes
        # Total d'attaques
        self.attacks_on_screen = (
            []
        )  # Contient toutes les instances des attaques du prof qui sont encore sur l'écran

    # ACCESSEURS
    # GETTERS

    def get_orientation(self):
        return self.orientation

    def get_vie(self):
        return self.vie

    def get_pos(self):
        return self.player_pos

    def get_dimensions(self):
        return (self.LONGUEUR, self.LARGEUR)

    def get_object_type(self):
        return self.type

    def get_current_attacks(self):
        return self.attacks_on_screen

    def get_crayon_cadence_de_tir(self):
        return self.crayon_cadence_de_tir

    def get_citation_cadence_de_tir(self):
        return self.crayon_cadence_de_tir

    def get_a_ete_touche(self):
        return self.a_ete_touche

    def get_hurt_timer(self):
        return self.hurt_timer

    # SETTERS

    def set_vie(self, vie: int):
        assert type(vie) == int, "La valeur de vie doît être entière."
        self.vie = vie

    def set_pos(self, pos: pygame.Vector2):
        assert (
            type(pos) == pygame.Vector2
        ), "La position doît être un vecteur à deux dimensions."
        self.pos = pos

    def set_orientation(self, orientation: str):
        assert type(orientation) == str and (
            orientation == "RIGHT" or orientation == "LEFT"
        ), "La valeur de l'orientation doît être une chaîne de caractères égale à 'RIGHT' ou 'LEFT'."
        self.orientation = orientation

    def set_crayon_cadence_de_tir(self, cadence: int):
        assert type(cadence) == int, "La cadence de tir donnée n'est pas un entier."
        self.crayon_cadence_de_tir = cadence

    def set_citation_cadence_de_tir(self, cadence: int):
        assert type(cadence) == int, "La cadence de tir donnée n'est pas un entier."
        self.citation_cadence_de_tir = cadence

    def set_a_ete_touche(self, a_ete_touche: bool):
        assert type(a_ete_touche) == bool, "La valeur indiquée doît être un booléen."
        self.a_ete_touche = a_ete_touche

    def set_hurt_time(self, timer: int):
        assert type(timer) == int, "La valeur indiquée doît être un entier."
        self.hurt_timer = timer

    # MÉTHODES

    def movement(self, dt: float, screen:pygame.Surface):
        """
        Permet de faire changer les coordonnées de l'instance du Prof, basé sur les commandes du clavier.\n
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement, 
        screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(dt) == float, "La valeur de delta t est invalide."
        assert type(screen) == pygame.Surface, "La surface est invalide."
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and self.player_pos.y >= 0:
            self.player_pos.y -= 500 * dt
        if (
            keys[pygame.K_s]
            and self.player_pos.y + self.LARGEUR <= screen.get_height() // 2
        ):
            self.player_pos.y += 500 * dt
        if keys[pygame.K_q] and self.player_pos.x >= 0:
            self.player_pos.x -= 400 * dt
            if self.orientation == "RIGHT":
                self.orientation = "LEFT"
                self.texture = pygame.transform.flip(self.texture.copy(), True, False)
        if keys[pygame.K_d] and self.player_pos.x + self.LONGUEUR <= screen.get_width():
            self.player_pos.x += 400 * dt
            if self.orientation == "LEFT":
                self.orientation = "RIGHT"
                self.texture = pygame.transform.flip(self.texture.copy(), True, False)

    def draw(self, screen:pygame.Surface):
        """
        Permet de dessiner à l'écran l'image de l'instance du Prof.\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        screen.blit(self.texture, self.player_pos)

    def attack_management(self):
        """
        Procédure permettant de gérer en continu les pressions de touches, qui activeront chacune des attaques respectives.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and (
            pygame.time.get_ticks() - self.last_crayon >= self.crayon_cadence_de_tir
        ):
            self.lance_crayon()
            self.last_crayon = pygame.time.get_ticks()
        if keys[pygame.K_g] and (
            pygame.time.get_ticks() - self.last_citation >= self.citation_cadence_de_tir
        ):
            self.lance_citation()
            self.last_citation = pygame.time.get_ticks()
        self.invincibilite()

    def lance_crayon(self):
        """
        Permet de lancer l'attaque 'crayon', en créant une nouvelle instance de Crayon à la liste des attaques courantes.
        """
        sfx = AllSounds()
        sfx.play_sfx("CRAYON", 1)
        self.attacks_on_screen.append(
            Crayon(
                (
                    self.player_pos.x + self.LONGUEUR // 2,
                    self.player_pos.y + self.LARGEUR - 10,
                ),
                "DOWN",
            )
        )

    def lance_citation(self):
        """
        Permet de lancer l'attaque 'citation', en créant une nouvelle instance de CitationLaser à la liste des attaques courantes.
        """
        self.attacks_on_screen.append(
            CitationLaser((self.player_pos.x, self.player_pos.y), "DOWN")
        )

    def affiche_hud(self, screen:pygame.Surface):
        """
        Permet d'afficher le HUD (affichage tête-haute).\n
        Paramètre:screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        font = pygame.font.Font("./Assets/Font/ARCADE_N.ttf", 20)
        font2 = pygame.font.Font("./Assets/Font/ARCADE_N.ttf", 12)
        text = font.render(f"Vie  {self.vie}", True, "black")
        if pygame.time.get_ticks() - self.last_crayon <= self.crayon_cadence_de_tir:
            crayon = font2.render(f"[F] {round(self.crayon_cadence_de_tir/1000-(pygame.time.get_ticks() - self.last_crayon)/1000, 1)}", True, "black")
        else:
            crayon = font2.render(f"[F] PRET", True, "green")
        if pygame.time.get_ticks() - self.last_citation <= self.citation_cadence_de_tir:
            citation = font2.render(f"[G] {round(self.citation_cadence_de_tir/1000-(pygame.time.get_ticks() - self.last_citation)/1000, 1)}", True, "black")
        else:
            citation = font2.render(f"[G] PRET", True, "green")
        screen.blit(text, (10, 20))
        screen.blit(crayon, (10, 55))
        screen.blit(citation, (10, 75))

    def est_mort(self):
        """
        Permet de détecter quand la vie de l'instance de la classe est inférieure ou égale à 0.\n
        Renvoie: tuple avec True et l'instance de la classe.
        """
        if self.vie <= 0:
            self.vie = 0
            return (True, self)
        else:
            return (False, self)

    def invincibilite(self):
        """
        Permet d'afficher une animation pendant un temps donné sur le personnage à chaque fois qu'il est touché par une attaque.
        """
        if self.a_ete_touche:
            start = self.hurt_timer
            if pygame.time.get_ticks() - start <= self.temps_invincible:
                sinus_val = round(math.sin((pygame.time.get_ticks() - start) / 100) + 1)
                if sinus_val >= 1:
                    self.texture = self.textures[1]
                elif sinus_val < 1:
                    self.texture = self.textures[0]
                    if self.orientation == "LEFT":
                        self.texture = pygame.transform.flip(
                            self.texture.copy(), True, False
                        )
            else:
                self.a_ete_touche = False
                self.hurt_timer = 0
                self.texture = self.textures[0]


class Eleve:
    def __init__(self, vie: int, pos: tuple[int], LONGUEUR: int, LARGEUR: int):
        assert type(vie) == int, "Un entier est attendu."
        assert type(pos) == tuple, "Un tuple de coordonnées est attendu."
        assert type(LONGUEUR) == int and type(LARGEUR) == int, "Des valeurs entières sont attendues pour les dimensions."
        self.vie = vie
        self.player_pos = pygame.Vector2(pos[0], pos[1])
        self.texture = pygame.image.load("./Assets/Textures/ELEVE_PIXEL.png")
        self.texture = pygame.transform.scale(self.texture, (81, 136))
        self.LONGUEUR, self.LARGEUR = LONGUEUR, LARGEUR

        self.orientation = "RIGHT"
        self.type = "ELEVE"
        # Crayon
        self.last_crayon = 0
        self.crayon_cadence_de_tir = 500  # Millisecondes
        # Table
        self.last_table = 0
        self.table_cadence = 5000  # Millisecondes
        # Animation
        self.a_ete_touche = False
        self.temps_invincible = 2500  # Millisecondes
        self.texture_hurt = pygame.image.load("./Assets/Textures/HURT.png")
        self.textures = [self.texture, self.texture_hurt]
        self.hurt_timer = 0

        # Total d'attaques
        self.attacks_on_screen = (
            []
        )  # Contient toutes les instances des attaques de l'Eleve qui sont encore sur l'écran.
        self.tables_on_screen = (
            []
        )  # Contient toutes les instances des tables de l'Eleve qui sont encore sur l'écran.

    # ACCESSEURS
    # GETTERS

    def get_orientation(self):
        return self.orientation

    def get_vie(self):
        return self.vie

    def get_pos(self):
        return self.player_pos

    def get_dimensions(self):
        return (self.LONGUEUR, self.LARGEUR)

    def get_object_type(self):
        return self.type

    def get_current_attacks(self):
        return self.attacks_on_screen

    def get_current_tables(self):
        return self.tables_on_screen

    def get_crayon_cadence_de_tir(self):
        return self.crayon_cadence_de_tir

    def get_a_ete_touche(self):
        return self.a_ete_touche

    def get_hurt_timer(self):
        return self.hurt_timer

    # SETTERS

    def set_vie(self, vie: int):
        assert type(vie) == int, "La valeur de vie doît être entière."
        self.vie = vie

    def set_pos(self, pos: pygame.Vector2):
        assert (
            type(pos) == pygame.Vector2
        ), "La position doît être un vecteur à deux dimensions."
        self.pos = pos
    
    def set_orientation(self, orientation: str):
        assert type(orientation) == str and (
            orientation == "RIGHT" or orientation == "LEFT"
        ), "La valeur de l'orientation doît être une chaîne de caractères égale à 'RIGHT' ou 'LEFT'."
        self.orientation = orientation

    def set_crayon_cadence_de_tir(self, cadence: int):
        assert type(cadence) == int, "La cadence de tir donnée n'est pas un entier."
        self.crayon_cadence_de_tir = cadence

    def set_a_ete_touche(self, a_ete_touche: bool):
        assert type(a_ete_touche) == bool, "La valeur indiquée doît être un booléen."
        self.a_ete_touche = a_ete_touche

    def set_hurt_time(self, timer: int):
        assert type(timer) == int, "La valeur indiquée doît être un entier."
        self.hurt_timer = timer

    # MÉTHODES

    def movement(self, dt: float, screen:pygame.Surface):
        """
        Permet de faire changer les coordonnées de l'instance de l'Eleve, basé sur les commandes du clavier.\n
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement, *
        screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe..
        """
        assert type(dt) == float, "La valeur de delta t est invalide."
        assert type(screen) == pygame.Surface, "La surface est invalide."
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_pos.y >= screen.get_height() // 2:
            self.player_pos.y -= 350 * dt
        if (
            keys[pygame.K_DOWN]
            and self.player_pos.y + self.LARGEUR <= screen.get_height()
        ):
            self.player_pos.y += 350 * dt
        if keys[pygame.K_LEFT] and self.player_pos.x >= 0:
            self.player_pos.x -= 350 * dt
            if self.orientation == "RIGHT":
                self.orientation = "LEFT"
                self.texture = pygame.transform.flip(self.texture.copy(), True, False)
        if (
            keys[pygame.K_RIGHT]
            and self.player_pos.x + self.LONGUEUR <= screen.get_width()
        ):
            self.player_pos.x += 350 * dt
            if self.orientation == "LEFT":
                self.orientation = "RIGHT"
                self.texture = pygame.transform.flip(self.texture.copy(), True, False)
        self.invincibilite()

    def draw(self, screen:pygame.Surface):
        """
        Permet de dessiner à l'écran l'image de l'instance de l'Eleve.\n
        Paramètre:screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        screen.blit(self.texture, self.player_pos)

    def attack_management(self, screen:pygame.Surface):
        """
        Procédure permettant de gérer en continu les pressions de touches, qui activeront chacune des attaques respectives.\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m] and (
            pygame.time.get_ticks() - self.last_crayon >= self.crayon_cadence_de_tir
        ):
            self.lance_crayon()
            self.last_crayon = pygame.time.get_ticks()
        if keys[pygame.K_l] and (
            pygame.time.get_ticks() - self.last_table >= self.table_cadence
        ) and (len(self.tables_on_screen) < 3):
            self.lance_table(screen)
            self.last_table = pygame.time.get_ticks()
        self.invincibilite()

    def lance_crayon(self):
        """
        Permet de lancer l'attaque 'crayon', en créant une nouvelle instance de Crayon à la liste des attaques courantes.
        """
        sfx = AllSounds()
        sfx.play_sfx("CRAYON", 2)
        self.attacks_on_screen.append(
            Crayon(((self.player_pos.x + self.LONGUEUR // 2), self.player_pos.y), "UP")
        )

    def lance_table(self, screen:pygame.Surface):
        """
        Permet de lancer l'attaque 'table', en créant une nouvelle instance de Table à la liste des attaques courantes.\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        if len(self.tables_on_screen) < 3:
            sfx = AllSounds()
            sfx.play_sfx("TABLE_BLOCK", 7)
            self.tables_on_screen.append(
                Table(((self.player_pos.x - 20), self.player_pos.y - 30), screen)
            )

    def affiche_hud(self, screen:pygame.surface):
        """
        Permet d'afficher le HUD (affichage tête-haute).\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        font = pygame.font.Font("./Assets/Font/ARCADE_N.ttf", 20)
        font2 = pygame.font.Font("./Assets/Font/ARCADE_N.ttf", 12)
        text = font.render(f"Vie  {self.vie}", True, "black")
        if pygame.time.get_ticks() - self.last_crayon <= self.crayon_cadence_de_tir:
            crayon = font2.render(f"[M] {round(self.crayon_cadence_de_tir/1000-(pygame.time.get_ticks() - self.last_crayon)/1000, 1)}", True, "black")
        else:
            crayon = font2.render(f"[M] PRET", True, "green")
        if pygame.time.get_ticks() - self.last_table <= self.table_cadence:
            table = font2.render(f"[L] {round(self.table_cadence/1000-(pygame.time.get_ticks() - self.last_table)/1000, 1)}", True, "black")
        else:
            color = "green" if len(self.tables_on_screen) < 3 else "red"
            table = font2.render(f"[L] PRET", True, color)

        screen.blit(text, (10, screen.get_height() - 50))
        screen.blit(table, (10, screen.get_height() - 85))
        screen.blit(crayon, (10, screen.get_height() - 105))

    def est_mort(self):
        """
        Permet de détecter quand la vie de l'instance de la classe est inférieure ou égale à 0.\n
        Renvoie: tuple avec True et l'instance de la classe.
        """
        if self.vie <= 0:
            self.vie = 0
            return (True, self)
        else:
            return (False, self)

    def invincibilite(self):
        """
        Permet d'afficher une animation pendant un temps donné sur le personnage à chaque fois qu'il est touché par une attaque.
        """
        if self.a_ete_touche:
            start = self.hurt_timer
            if pygame.time.get_ticks() - start <= self.temps_invincible:
                sinus_val = round(math.sin((pygame.time.get_ticks() - start) / 100) + 1)
                if sinus_val >= 1:
                    self.texture = self.textures[1]
                elif sinus_val < 1:
                    self.texture = self.textures[0]
                    if self.orientation == "LEFT":
                        self.texture = pygame.transform.flip(
                            self.texture.copy(), True, False
                        )
            else:
                self.a_ete_touche = False
                self.hurt_timer = 0
                self.texture = self.textures[0]


class Table:
    def __init__(self, pos: tuple, screen:pygame.Surface):
        assert type(pos) == tuple, "Un tuple de coordonnées est attendu."
        assert type(screen) == pygame.Surface, "La surface est invalide."
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.texture = pygame.image.load("./Assets/Textures/TABLE.png")
        self.texture = pygame.transform.scale(self.texture, (130, 77))
        if self.pos.x >= screen.get_width() // 2 - self.texture.get_width()//2:
            self.texture = pygame.transform.flip(self.texture.copy(), True, False)
        self.LONGUEUR, self.LARGEUR = (
            self.texture.get_width(),
            self.texture.get_height(),
        )
        self.attaques_absorbables = 3
        self.destructible = False
        self.type = "TABLE"

    # ACCESSEURS
    # GETTERS

    def get_orientation(self):
        return self.orientation

    def get_destructible(self):
        return self.vie

    def get_pos(self):
        return self.pos

    def get_object_type(self):
        return self.type

    def get_dimensions(self):
        return (self.LONGUEUR, self.LARGEUR)

    def get_attaques_absorbables(self):
        return self.attaques_absorbables

    # SETTERS

    def set_destructible(self, destructible: bool):
        assert (
            type(destructible) == bool
        ), "L'argument en paramètre doît être un booléen."
        self.destructible = destructible

    def set_attaques_absorbables(self, att: int):
        assert type(att) == int, "Le nombre d'attaques doît être un nombre entier."
        self.attaques_absorbables = att

    # MÉTHODES

    def draw(self, screen:pygame.Surface):
        """
        Permet de dessiner à l'écran l'image de l'instance de la table.\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        screen.blit(self.texture, self.pos)

    def supprimer_dechets(self, table_list:list, index:int):
        """
        Supprime l'instance de la classe si elle complète les critères nécessaires.\n
        Paramètres:\n
        - table_list: liste contenant des instances de la classe Table. _n
        - index: nombre entier entre 0 et len(table_list).
        """
        assert type(table_list) == list, "table_list doît être une liste."
        assert (
            type(index) == int and 0 <= index and index <= len(table_list)
        ), "La valeur de index doît être un nombre entier, compris entre 0 et len(object_list)."
        if self.attaques_absorbables <= 0:
            self.destructible = True
        if self.destructible:
            table_list.pop(index)


class Crayon:
    def __init__(self, pos: tuple, direction: str):
        assert type(pos) == tuple, "Un tuple de coordonnées est attendu."
        assert type(direction) == str and (
            direction == "UP" or direction == "DOWN"
        ), "La valeur de l'orientation doît être une chaîne de caractères égale à 'DOWN' ou 'UP'."
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.direction = direction
        self.texture = pygame.image.load("./Assets/Textures/PENCIL_PIXEL.png")
        self.texture = pygame.transform.scale(self.texture, (13, 90))
        self.degats = 10
        self.destructible = False
        self.type = "CRAYON"

    # ACCESSEURS
    # GETTERS

    def get_orientation(self):
        return self.orientation

    def get_destructible(self):
        return self.vie

    def get_pos(self):
        return self.player_pos

    def get_object_type(self):
        return self.type

    # SETTERS

    def set_orientation(self, orientation: str):
        assert type(orientation) == str and (
            orientation == "UP" or orientation == "DOWN"
        ), "La valeur de l'orientation doît être une chaîne de caractères égale à 'UP' ou 'DOWN'."
        self.orientation = orientation

    def set_destructible(self, destructible: bool):
        assert (
            type(destructible) == bool
        ), "L'argument en paramètre doît être un booléen."
        self.destructible = destructible
    
    # MÉTHODES

    def draw(self, screen:pygame.Surface):
        """
        Permet de dessiner à l'écran l'image de l'instance du crayon.\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        if self.direction == "UP":
            self.texture = pygame.transform.flip(self.texture.copy(), False, True)
        screen.blit(self.texture, self.pos)

    def movement(self, dt: float, screen:pygame.Surface):
        """
        Permet de faire changer les coordonnées de l'instance du crayon par rapport à son orientation prédéterminée et sa vitesse.\n
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement, 
        screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(dt) == float, "La valeur de delta t est invalide."
        assert type(screen) == pygame.Surface, "La surface est invalide."
        if self.direction == "UP":
            self.pos.y -= 500 * dt
        else:
            self.pos.y += 700 * dt
        if (
            self.pos.y > screen.get_height()
            or self.pos.y + self.texture.get_height() < 0
        ):
            self.destructible = True

    def supprimer_dechets(self, object_list: list, index: int):
        """
        Supprime l'instance de la classe si elle complète les critères nécessaires.\n
        Paramètres:\n
        - object_list: liste contenant des instances de Classes telles que Crayon et CitationLaser.\n
        - index: nombre entier entre 0 et len(object_list).
        """
        assert type(object_list) == list, "object_list doît être une liste."
        assert (
            type(index) == int and 0 <= index and index <= len(object_list)
        ), "La valeur de index doît être un nombre entier, compris entre 0 et len(object_list)."
        if self.destructible:
            object_list.pop(index)

    def collisions(self, player, table_list:list[Table]):
        """
        Prend en charge les collisions entre cette instance du crayon et toutes les instances de la classe Table ainsi que
        de la classe Joueur encores présentes sur l'écran.\n
        Paramètres:\n
        - eleve: instance de la classe Eleve ou Prof.\n
        - table_list: liste contenant des instances de la classe Table, ou liste vide.
        """
        assert (
            type(player) == Eleve or type(player) == Prof
        ), "Une instance de la classe Eleve ou Prof est attendue en premier paramètre."
        assert type(table_list) == list and (
            len(table_list) == 0 or type(table_list[0]) == Table
        ), "Une liste vide ou contenant des instances de la classe Table est attendue."
        sfx = AllSounds()
        # Collision avec l'élève ou la table
        if self.direction == "DOWN":
            xpos_matches_eleve = (
                int(player.get_pos().x)
                <= self.pos.x
                <= int(player.get_pos().x + player.get_dimensions()[0])
            )
            ypos_matches_eleve = (
                int(player.get_pos().y)
                <= self.pos.y + self.texture.get_height()
                <= int(player.get_pos().y + player.get_dimensions()[1])
            )
            for table in table_list:
                xpos_matches_table = (
                    int(table.get_pos().x)
                    <= self.pos.x
                    <= int(table.get_pos().x + table.get_dimensions()[0])
                )
                ypos_matches_table = (
                    int(table.get_pos().y)
                    <= self.pos.y + self.texture.get_height()
                    <= int(player.get_pos().y + player.get_dimensions()[1])
                )
                if xpos_matches_table and ypos_matches_table:
                    self.destructible = True
                    table.set_attaques_absorbables(table.get_attaques_absorbables() - 1)
                    sfx.play_sfx("TABLE_BLOCK", 2)
            if (
                xpos_matches_eleve
                and ypos_matches_eleve
                and (not player.get_a_ete_touche())
            ):
                self.destructible = True
                player.set_vie(player.get_vie() - self.degats)
                player.set_a_ete_touche(True)
                player.set_hurt_time(pygame.time.get_ticks())
                sfx.play_sfx("HURT_ELEVE", 3)
        # Collision avec le Prof
        elif self.direction == "UP":
            xpos_matches_prof = (
                int(player.get_pos().x)
                <= self.pos.x
                <= int(player.get_pos().x + player.get_dimensions()[0])
            )
            ypos_matches_prof = (
                int(player.get_pos().y)
                <= self.pos.y
                <= int(player.get_pos().y + player.get_dimensions()[1])
            )
            if (
                xpos_matches_prof
                and ypos_matches_prof
                and (not player.get_a_ete_touche())
            ):
                self.destructible = True
                player.set_vie(player.get_vie() - self.degats * 2)
                player.set_a_ete_touche(True)
                player.set_hurt_time(pygame.time.get_ticks())
                sfx.play_sfx("HURT_PROF", 4)


class AllSounds:
    def __init__(self):
        # Définit les chemins de tous les sound effects et musiques, ainsi que le nombre de variantes disponibles (inutilisé)
        self.dico_sounds = {"HURT_ELEVE": 1, "HURT_PROF": 1, "LASER": 1, "TABLE_BLOCK": 1, "GAME_OVER": 1, "RESTART": 1, "CRAYON": 1}
        self.common_path = "./Assets/Sons/"

    # Jouer un sound effect
    def play_sfx(self, son: str, channel_id:int):
        """
        Joue un son parmi ceux qui existent dans cette classe.\n
        Paramètre: son (str), nom du sound_effect qui sera joué, channel_id (int) entre 1 et 7 qui va définir le channel sur lequel le son va être joué.
        """
        assert type(son) == str, "Le nom de l'effet sonore à jouer est invalide."
        assert type(channel_id) == int and 1 <= channel_id <= 7, "Un id de channel entier est attendu entre 1 et 7."
        son = son.upper()
        if son in self.dico_sounds.keys() and self.dico_sounds[son] >= 0:
            sound = pygame.mixer.Sound(
                f"{self.common_path}{son}_{random.randint(0,self.dico_sounds[son]-1)}.mp3"
            )
            channel = pygame.mixer.Channel(channel_id)
            channel.play(sound)
    

class CitationLaser:
    def __init__(self, pos: tuple, direction: str):
        assert type(pos) == tuple, "Un tuple de coordonnées est attendu."
        assert type(direction) == str and (
            direction == "UP" or direction == "DOWN"
        ), 'La direction doît être une chaîne de caractères telle que "DOWN" ou "UP".'
        self.texture = pygame.image.load(
            f"./Assets/Textures/Citations/cit_{random.randint(0,11)}.png"
        )
        self.texture = pygame.transform.rotate(self.texture, 90)
        self.texture = pygame.transform.scale(
            self.texture, (self.texture.get_width() * 6, self.texture.get_height() * 6)
        )
        self.destructible = False
        self.temps_inoffensif = 1500  # Millisecondes
        self.temps_existant = 4250    # Millisecondes
        self.temps_apparition = pygame.time.get_ticks()
        self.rect_color = "magenta"
        self.degats_actifs = False
        self.a_touche_joueur = False
        self.degats = 50
        self.type = "CITATION"
        self.pos = pygame.Vector2(pos[0] + 10, pos[1])
        self.texture_pos = pygame.Vector2(
            self.pos.x + 10, 0 - self.texture.get_height() - self.pos.y
        )
        self.direction = direction
        sfx = AllSounds()
        sfx.play_sfx("LASER", 5)
    
    # ACCESSEURS
    # GETTERS

    def get_destructible(self):
        return self.vie

    def get_pos(self):
        return self.player_pos

    def get_object_type(self):
        return self.type

    def get_degats_actifs(self):
        return self.degats_actifs

    # SETTERS

    def set_destructible(self, destructible: bool):
        assert (
            type(destructible) == bool
        ), "L'argument en paramètre doît être un booléen."
        self.destructible = destructible

    # MÉTHODES

    def draw(self, screen:pygame.Surface):
        """
        Permet de dessiner à l'écran l'image de l'instance de la citation.\n
        Paramètre: screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(screen) == pygame.Surface, "La surface est invalide."
        pygame.draw.rect(
            screen,
            self.rect_color,
            pygame.Rect(
                (self.pos.x, 0), (self.texture.get_width() + 10, screen.get_height())
            ),
        )
        screen.blit(self.texture, self.texture_pos)

    def movement(self, dt: float, screen:pygame.Surface):
        """
        Permet de faire changer les coordonnées de l'instance de la citation par rapport à sa direction prédeterminée et sa vitesse.\n
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement, 
        screen (pygame.Surface) surface sur laquelle imprimer l'instance de la classe.
        """
        assert type(dt) == float, "La valeur de delta t est invalide."
        assert type(screen) == pygame.Surface, "La surface est invalide."
        if (
            pygame.time.get_ticks() - self.temps_apparition >= self.temps_inoffensif
            and not self.a_touche_joueur
        ):
            self.degats_actifs = True
            self.rect_color = "red"
        if pygame.time.get_ticks() - self.temps_apparition >= self.temps_inoffensif:
            self.texture_pos.y += 1250 * dt
        if self.pos.y > screen.get_height():
            self.destructible = True
        if pygame.time.get_ticks() - self.temps_apparition >= self.temps_existant:
            self.destructible = True

    def supprimer_dechets(self, object_list: list, index: int):
        """
        Supprime l'instance de la classe si elle complète les critères nécessaires.
        Paramètres:
        - object_list: liste contenant des instances de Classes telles que Crayon et CitationLaser.
        - index: nombre entier entre 0 et len(object_list).
        """
        assert type(object_list) == list, "object_list doît être une liste."
        assert (
            type(index) == int and 0 <= index and index <= len(object_list)
        ), "La valeur de index doît être un nombre entier, compris entre 0 et len(object_list)."
        if self.destructible:
            if (
                0
                <= pygame.time.get_ticks() - self.temps_apparition - self.temps_existant
                <= 200
            ):
                self.retrecir(self.temps_existant + self.temps_apparition, 300)
            elif (
                pygame.time.get_ticks() - self.temps_apparition
                <= self.temps_existant - 2500
            ):
                self.retrecir(self.temps_apparition + self.temps_inoffensif, 300)
            else:
                object_list.pop(index)

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
        assert (
            type(temps_soutrait) == int
        ), "Le temps soustrait n'est pas un entier (positif de préférence)."
        assert (
            type(duree_fonction) == int and duree_fonction > 0
        ), "La durée de la fonction (en ms) est invalide."
        easeout_val = math.sqrt(
            1 - ((pygame.time.get_ticks() - temps_soutrait) / duree_fonction) ** 2
        )  # Fonction Ease-out Circulaire
        if easeout_val != 0:
            self.texture = pygame.transform.scale(
                self.texture,
                (self.texture.get_width() * easeout_val, self.texture.get_height()),
            )
            self.texture_pos.x += easeout_val / 2
            self.pos.x += easeout_val / 2
            return True
        else:
            return False

    def collisions(self, player: Eleve, table_list: list[Table]):
        """
        Prend en charge les collisions entre cette instance de la citation et toutes les instances de la classe Table ainsi que
        de la classe Joueur encores présentes sur l'écran.\n
        Paramètres:\n
        - eleve: instance de la classe Eleve.\n
        - table_list: liste contenant des instances de la classe Table, ou liste vide.
        """
        assert (
            type(player) == Eleve
        ), "Une instance de la classe Eleve est attendue en premier paramètre."
        assert type(table_list) == list and (
            len(table_list) == 0 or type(table_list[0]) == Table
        ), "Une liste vide ou contenant des instances de la classe Table est attendue."
        sfx = AllSounds()
        xleftpos_matches_player = (
            int(player.get_pos().x)
            <= self.pos.x
            <= int(player.get_pos().x + player.get_dimensions()[0])
        )
        xrightpos_matches_player = (
            int(player.get_pos().x)
            <= self.pos.x + self.texture.get_width() + 10
            <= int(player.get_pos().x + player.get_dimensions()[0])
        )
        # Collision avec une table
        for table in table_list:
            xleftpos_matches_table = (
                int(table.get_pos().x)
                <= self.pos.x
                <= int(table.get_pos().x + table.get_dimensions()[0])
            )
            xrightpos_matches_table = (
                int(table.get_pos().x)
                <= self.pos.x + self.texture.get_width() + 10
                <= int(table.get_pos().x + table.get_dimensions()[0])
            )
            if (
                xleftpos_matches_table or xrightpos_matches_table
            ) and self.degats_actifs:
                self.a_touche_joueur = True
                table.set_attaques_absorbables(table.get_attaques_absorbables() - 2)
                self.degats_actifs = False
                self.destructible = True
                sfx.play_sfx("TABLE_BLOCK", 2)
        # Collision avec l'élève
        if (
            xleftpos_matches_player or xrightpos_matches_player
        ) and self.degats_actifs:
            self.degats_actifs = False
            self.a_touche_joueur = True
            player.set_vie(player.get_vie() - self.degats)
            player.set_a_ete_touche(True)
            player.set_hurt_time(pygame.time.get_ticks())
            sfx.play_sfx("HURT_ELEVE", 3)


class Main:
    def __init__(self, LONGUEUR:int, LARGEUR:int):
        assert type(LONGUEUR) == int and type(LARGEUR) == int, "Des entiers sont attendus pour les dimensions de l'écran."
        # Initialisation du jeu
        pygame.init()
        # Écran
        self.LONGUEUR = LONGUEUR
        self.LARGEUR = LARGEUR
        self.screen = pygame.display.set_mode(
            (self.LONGUEUR, self.LARGEUR)
        )
        pygame.display.set_caption("Filosofight")
        pygame.display.set_icon(pygame.image.load("./icon.png"))
        self.background = pygame.image.load("./Assets/Textures/BACKGROUND.png")

        # Timer et fonctionnement du jeu
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = True
        self.delta_t = 0.0
        self.gagnant = ""
        self.soissantièmes = 60
        self.secondes = 29
        self.minutes = 2

        # Création de l'élève et du prof
        self.prof = Prof(500, (self.LONGUEUR // 2, self.LARGEUR // 4), 132, 132)
        self.eleve = Eleve(200, (self.LONGUEUR // 2, (self.LARGEUR // 4) * 3), 81, 136)

        # Son de départ
        sfx = AllSounds()
        sfx.play_sfx("RESTART", 6)
        

    # MÉTHODES

    def is_game_over(self):
        """
        Fonction qui renvoie True ou False si l'un des joueurs meurt. Dans le cas où la fonction renvoie True, elle change
        aussi la valeur de gagnant pour indiquer le nom du gagnant.
        """
        sfx = AllSounds()
        if self.prof.est_mort()[0]:
            gagnant = self.eleve.est_mort()[1].get_object_type()
            sfx.play_sfx("GAME_OVER", 6)
            return False, gagnant
        elif self.eleve.est_mort()[0]:
            gagnant = self.prof.est_mort()[1].get_object_type()
            sfx.play_sfx("GAME_OVER", 6)
            return False, gagnant
        elif self.minutes <= 0 and self.secondes >= 55:
            gagnant = "PROF"
            sfx.play_sfx("GAMEOVER", 6)
            return False, gagnant
        else:
            return True, ""

    def restart_manager(self):
        """
        Quand elle est appelée, cette méthode attend l'appui de la touche R pour réinitialiser le jeu à zéro.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.__init__(self.LONGUEUR, self.LARGEUR)
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def timer(self):
        """
        Prend en charge le calcul du temps et l'affichage du temps sur l'affichage tête haute.
        """
        # chronomètre
        self.soissantièmes -= 1
        if self.soissantièmes == 0:
            self.secondes -= 1
            self.soissantièmes = 60
        if self.secondes == 0:
            self.minutes -= 1
            self.secondes = 59
        font = pygame.font.Font("./Assets/Font/ARCADE_N.ttf", 15)
        text = font.render(f"TIME {self.minutes}:{self.secondes}", True, "white")
        self.screen.blit(text, (10, self.LARGEUR//2+text.get_height()//2+80))

    def game(self):
        """
        Déroulement du jeu dans toute son intégralité. (boucle while)
        """
        # Boucle principale
        while self.running:
            # Boucle des évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.playing:
                self.playing, self.gagnant = self.is_game_over()
            # On remplit l'écran avec le fond d'écran pour tout effacer
            self.screen.blit(self.background, (0,0))


            if self.playing:
                # Timer
                self.time_fin = time.time()
                # Affichage des images (joueurs)
                self.prof.draw(self.screen)
                self.eleve.draw(self.screen)

                # Mouvement des images (joueurs)
                self.prof.movement(self.delta_t, self.screen)
                self.eleve.movement(self.delta_t, self.screen)

                # Gestion des attaques & collisions
                self.prof.attack_management()
                self.eleve.attack_management(self.screen)

                # Dans l'ordre: Affichage, mouvement, puis collisions des attaques du Prof et de l'Eleve (+ fonctionnement des Tables)
                for object in self.prof.get_current_attacks():
                    object.draw(self.screen)
                    object.movement(self.delta_t, self.screen)
                    object.collisions(
                        self.eleve, self.eleve.get_current_tables()
                    )  # Collisions des attaques du prof avec l'élève
                for object in self.eleve.get_current_attacks():
                    object.draw(self.screen)
                    object.movement(self.delta_t, self.screen)
                    object.collisions(
                        self.prof, self.eleve.get_current_tables()
                    )  # Collisions des attaques de l'élève avec le prof
                for object in self.eleve.get_current_tables():
                    object.draw(self.screen)

                # Gestion des objets déchets à supprimer
                # Pour le Prof
                for object_index in range(len(self.prof.get_current_attacks())):
                    try:
                        self.prof.get_current_attacks()[object_index].supprimer_dechets(
                            self.prof.get_current_attacks(), object_index
                        )
                    except:
                        pass  # La suppression essaye parfois de supprimer un objet en dehors de la liste. Pour contrer le problème, on saute une frame pour supprimer l'objet à la frame suivante.
                # Pour l'Eleve - Attaques
                for object_index in range(len(self.eleve.get_current_attacks())):
                    try:
                        self.eleve.get_current_attacks()[object_index].supprimer_dechets(
                            self.eleve.get_current_attacks(), object_index
                        )
                    except:
                        pass  # La suppression essaye parfois de supprimer un objet en dehors de la liste. Pour contrer le problème, on saute une frame pour supprimer l'objet à la frame suivante.
                # Pour l'Eleve - Tables
                for object_index in range(len(self.eleve.get_current_tables())):
                    try:
                        self.eleve.get_current_tables()[object_index].supprimer_dechets(
                            self.eleve.get_current_tables(), object_index
                        )
                    except:
                        pass  # La suppression essaye parfois de supprimer un objet en dehors de la liste. Pour contrer le problème, on saute une frame pour supprimer l'objet à la frame suivante.

            # Affichage HUD (Affichage Tête-Haute)
            self.prof.affiche_hud(self.screen)
            self.eleve.affiche_hud(self.screen)
            if self.playing:
                self.timer()

            # Cas de game over
            if not self.playing:
                font = pygame.font.Font("./Assets/Font/ARCADE_N.ttf", 32)
                font2 = pygame.font.Font("./Assets/Font/ARCADE_N.ttf", 25)
                font3 = pygame.font.Font("./Assets/Font/ARCADE_N.ttf", 15)
                text = font.render(f"GAME OVER", True, "black",)
                text2 = font2.render(f"{self.gagnant} WINS", True, "black")
                text3 = font3.render(f"[R] POUR RESTART", True, "black")
                bac = pygame.transform.scale(pygame.image.load("./Assets/Textures/BAC.png"), (2000//4,1414//4))
                if self.gagnant == "ELEVE":
                    self.screen.blit(bac, (self.LONGUEUR//2-bac.get_width()//2, 300))
                self.screen.blit(text, (self.LONGUEUR//2-(text.get_width()//2), self.LARGEUR//2-(text.get_height()//2)-150))
                self.screen.blit(text2, (self.LONGUEUR//2-(text2.get_width()//2), self.LARGEUR//2-(text2.get_height()//2)+text.get_height()-150))
                self.screen.blit(text3, (self.LONGUEUR//2-(text3.get_width()//2), self.LARGEUR//2-(text3.get_height()//2)+2*text.get_height()-150))
                self.restart_manager()

            # flip() met à jour l'écran après l'affichage des images
            pygame.display.flip()

            # Delta t est le temps écoulé depuis la dernière frame
            self.delta_t = self.clock.tick(60) / 1000
        pygame.quit()


### PROGRAMME

main = Main(1280, 720)
main.game()
