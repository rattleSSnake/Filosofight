import pygame
import random
import math


class Prof:
    def __init__(self, vie: int, pos: tuple[int], LONGUEUR: int, LARGEUR: int):
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
        self.texture_hurt = pygame.image.load("./Assets/Textures/HURT.png").convert()
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

    def movement(self, dt: float):
        """
        Permet de faire changer les coordonnées de l'instance du Prof, basé sur les commandes du clavier.
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement.
        """
        assert type(dt) == float, "La valeur de delta t est invalide."
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and self.player_pos.y >= 0:
            self.player_pos.y -= 300 * dt
        if (
            keys[pygame.K_s]
            and self.player_pos.y + self.LARGEUR <= screen.get_height() // 2
        ):
            self.player_pos.y += 300 * dt
        if keys[pygame.K_q] and self.player_pos.x >= 0:
            self.player_pos.x -= 300 * dt
            if self.orientation == "RIGHT":
                self.orientation = "LEFT"
                self.texture = pygame.transform.flip(self.texture.copy(), True, False)
        if keys[pygame.K_d] and self.player_pos.x + self.LONGUEUR <= screen.get_width():
            self.player_pos.x += 300 * dt
            if self.orientation == "LEFT":
                self.orientation = "RIGHT"
                self.texture = pygame.transform.flip(self.texture.copy(), True, False)

    def draw(self):
        """
        Permet de dessiner à l'écran l'image de l'instance du Prof.
        """
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

    def affiche_hud(self):
        """
        Permet d'afficher le HUD (affichage tête-haute).
        """
        font = pygame.font.Font("./Assets/Font/ARCADECLASSIC.ttf", 32)
        text = font.render(f"Vie    {self.vie}", True, "white", "black")
        screen.blit(text, (10, 20))

    def est_mort(self):
        """
        Permet de détecter quand la vie de l'instance de la classe est inférieure ou égale à 0.
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

    def movement(self, dt: float):
        """
        Permet de faire changer les coordonnées de l'instance de l'Eleve, basé sur les commandes du clavier.
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement.
        """
        assert type(dt) == float, "La valeur de delta t est invalide."
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_pos.y >= screen.get_height() // 2:
            self.player_pos.y -= 300 * dt
        if (
            keys[pygame.K_DOWN]
            and self.player_pos.y + self.LARGEUR <= screen.get_height()
        ):
            self.player_pos.y += 300 * dt
        if keys[pygame.K_LEFT] and self.player_pos.x >= 0:
            self.player_pos.x -= 300 * dt
            if self.orientation == "RIGHT":
                self.orientation = "LEFT"
                self.texture = pygame.transform.flip(self.texture.copy(), True, False)
        if (
            keys[pygame.K_RIGHT]
            and self.player_pos.x + self.LONGUEUR <= screen.get_width()
        ):
            self.player_pos.x += 300 * dt
            if self.orientation == "LEFT":
                self.orientation = "RIGHT"
                self.texture = pygame.transform.flip(self.texture.copy(), True, False)
        self.invincibilite()

    def draw(self):
        """
        Permet de dessiner à l'écran l'image de l'instance de l'Eleve.
        """
        screen.blit(self.texture, self.player_pos)

    def attack_management(self):
        """
        Procédure permettant de gérer en continu les pressions de touches, qui activeront chacune des attaques respectives.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m] and (
            pygame.time.get_ticks() - self.last_crayon >= self.crayon_cadence_de_tir
        ):
            self.lance_crayon()
            self.last_crayon = pygame.time.get_ticks()
        if keys[pygame.K_l] and (
            pygame.time.get_ticks() - self.last_table >= self.table_cadence
        ):
            self.lance_table()
            self.last_table = pygame.time.get_ticks()

        self.invincibilite()

    def lance_crayon(self):
        """
        Permet de lancer l'attaque 'crayon', en créant une nouvelle instance de Crayon à la liste des attaques courantes.
        """
        self.attacks_on_screen.append(
            Crayon(((self.player_pos.x + self.LONGUEUR // 2), self.player_pos.y), "UP")
        )

    def lance_table(self):
        """
        Permet de lancer l'attaque 'table', en créant une nouvelle instance de Table à la liste des attaques courantes.
        """
        self.tables_on_screen.append(
            Table(((self.player_pos.x - 20), self.player_pos.y - 30))
        )

    def affiche_hud(self):
        """
        Permet d'afficher le HUD (affichage tête-haute).
        """
        font = pygame.font.Font("./Assets/Font/ARCADECLASSIC.ttf", 32)
        text = font.render(f"Vie    {self.vie}", True, "white", "black")
        screen.blit(text, (10, screen.get_height() - 50))

    def est_mort(self):
        """
        Permet de détecter quand la vie de l'instance de la classe est inférieure ou égale à 0.
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
    def __init__(self, pos: tuple):
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.texture = pygame.image.load("./Assets/Textures/TABLE.png")
        self.texture = pygame.transform.scale(self.texture, (130, 77))
        if self.pos.x >= screen.get_width() // 2:
            self.texture = pygame.transform.flip(self.texture.copy(), True, False)
        self.LONGUEUR, self.LARGEUR = (
            self.texture.get_width(),
            self.texture.get_height(),
        )
        self.attaques_absorbables = 3
        self.destructible = False
        self.type = "TABLE"

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

    def set_destructible(self, destructible: bool):
        assert (
            type(destructible) == bool
        ), "L'argument en paramètre doît être un booléen."
        self.destructible = destructible

    def set_attaques_absorbables(self, att: int):
        assert type(att) == int, "Le nombre d'attaques doît être un nombre entier."
        self.attaques_absorbables = att

    def draw(self):
        """
        Permet de dessiner à l'écran l'image de l'instance de la table.
        """
        screen.blit(self.texture, self.pos)

    def supprimer_dechets(self, table_list: list, index: int):
        """
        Supprime l'instance de la classe si elle complète les critères nécessaires.
        Paramètres:
        - table_list: liste contenant des instances de la classe Table.
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


class Livre:
    def __init__(self):
        self.type = "LIVRE"


class Crayon:
    def __init__(self, pos: tuple, direction: str):
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.direction = direction
        self.texture = pygame.image.load("./Assets/Textures/PENCIL_PIXEL.png")
        self.texture = pygame.transform.scale(self.texture, (13, 90))
        self.degats = 10
        self.destructible = False
        self.type = "CRAYON"

    def get_orientation(self):
        return self.orientation

    def get_destructible(self):
        return self.vie

    def get_pos(self):
        return self.player_pos

    def get_object_type(self):
        return self.type

    def set_orientation(self, orientation: str):
        assert type(orientation) == str and (
            orientation == "RIGHT" or orientation == "LEFT"
        ), "La valeur de l'orientation doît être une chaîne de caractères égale à 'RIGHT' ou 'LEFT'."
        self.orientation = orientation

    def set_destructible(self, destructible: bool):
        assert (
            type(destructible) == bool
        ), "L'argument en paramètre doît être un booléen."
        self.destructible = destructible

    def draw(self):
        """
        Permet de dessiner à l'écran l'image de l'instance du crayon.
        """
        if self.direction == "UP":
            self.texture = pygame.transform.flip(self.texture.copy(), False, True)
        screen.blit(self.texture, self.pos)

    def movement(self, dt: float):
        """
        Permet de faire changer les coordonnées de l'instance du crayon par rapport à son orientation prédéterminée et sa vitesse.
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement.
        """
        assert type(dt) == float, "La valeur de delta t est invalide."
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
            object_list.pop(index)

    def collisions(self, player, table_list: list[Table]):
        """
        Prend en charge les collisions entre cette instance du crayon et toutes les instances de la classe Table ainsi que
        de la classe Joueur encores présentes sur l'écran.
        Paramètres:
        - eleve: instance de la classe Eleve ou Prof.
        - table_list: liste contenant des instances de la classe Table, ou liste vide.
        """
        assert (
            type(player) == Eleve or type(player) == Prof
        ), "Une instance de la classe Eleve ou Prof est attendue en premier paramètre."
        assert type(table_list) == list and (
            len(table_list) == 0 or type(table_list[0]) == Table
        ), "Une liste vide ou contenant des instances de la classe Table est attendue."
        sfx = AllSounds()
        # Collision avec l'élève
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
            if (
                xpos_matches_eleve
                and ypos_matches_eleve
                and (not player.get_a_ete_touche())
            ):
                self.destructible = True
                player.set_vie(player.get_vie() - self.degats)
                player.set_a_ete_touche(True)
                player.set_hurt_time(pygame.time.get_ticks())
                sfx.play_sfx("HURT_ELEVE")
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
                sfx.play_sfx("HURT_PROF")


class AllSounds:
    def __init__(self):
        # Définir chemins des tous les sound effects et musiques
        self.dico_sounds = {"HURT_ELEVE": 0, "HURT_PROF": 0}
        self.common_path = "./Assets/Sons/"

    # Jouer un sound effect
    def play_sfx(self, son: str):
        """
        Joue un son parmi ceux qui existent dans cette classe.
        Paramètre: son (str), nom du sound_effect qui sera joué.
        """
        assert type(son) == str, "Le nom de l'effet sonore à jouer est invalide."
        son = son.upper()
        if son in self.dico_sounds.keys() and self.dico_sounds[son] >= 0:
            sound = pygame.mixer.Sound(
                f"{self.common_path}{son}_{random.randint(0,self.dico_sounds[son])}.mp3"
            )
            sound.play()


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
        self.temps_existant = 4250
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

    def get_orientation(self):
        return self.orientation

    def get_destructible(self):
        return self.vie

    def get_pos(self):
        return self.player_pos

    def get_object_type(self):
        return self.type

    def get_degats_actifs(self):
        return self.degats_actifs

    def set_orientation(self, orientation: str):
        assert type(orientation) == str and (
            orientation == "RIGHT" or orientation == "LEFT"
        ), "La valeur de l'orientation doît être une chaîne de caractères égale à 'RIGHT' ou 'LEFT'."
        self.orientation = orientation

    def set_destructible(self, destructible: bool):
        assert (
            type(destructible) == bool
        ), "L'argument en paramètre doît être un booléen."
        self.destructible = destructible

    def draw(self):
        """
        Permet de dessiner à l'écran l'image de l'instance de la citation.
        """
        pygame.draw.rect(
            screen,
            self.rect_color,
            pygame.Rect(
                (self.pos.x, 0), (self.texture.get_width() + 10, screen.get_height())
            ),
        )
        screen.blit(self.texture, self.texture_pos)

    def movement(self, dt: float):
        """
        Permet de faire changer les coordonnées de l'instance de la citation par rapport à sa direction prédeterminée et sa vitesse.
        Paramètre: dt (float), delta t (temps s'étant écoulé depuis la dernière frame), sert de coefficient pour le mouvement.
        """
        assert type(dt) == float, "La valeur de delta t est invalide."
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
        l'instance de la classe de l'écran, à l'aide d'une fonction ease-out circulaire.
        Paramètres:
        - temps_soustrait (int) -> Le temps à soustraire depuis l'apparition de l'instance de la classe jusqu'à l'instant présent
        afin que la variable x de la fonction ease-out commence de préférence à 0.
        - duree_fonction (int) -> Durée (en millisecondes) que devrait prendre en charge la fonction f.
        Pré-conditions:
        - temps_soustrait doît être de type int.
        - duree_fonction doît être de type int, strictement supérieure à 0.
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
        de la classe Joueur encores présentes sur l'écran.
        Paramètres:
        - eleve: instance de la classe Eleve.
        - table_list: liste contenant des instances de la classe Table, ou liste vide.
        """
        assert (
            type(player) == Eleve
        ), "Une instance de la classe Eleve est attendue en premier paramètre."
        assert type(table_list) == list and (
            len(table_list) == 0 or type(table_list[0]) == Table
        ), "Une liste vide ou contenant des instances de la classe Table est attendue."
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
            else:
                if (
                    xleftpos_matches_player or xrightpos_matches_player
                ) and self.degats_actifs:
                    self.degats_actifs = False
                    self.a_touche_joueur = True
                    player.set_vie(player.get_vie() - self.degats)
                    player.set_a_ete_touche(True)
                    player.set_hurt_time(pygame.time.get_ticks())


class Main:
    def __init__(self):
        pass


# Initialisation du jeu
pygame.init()
# Écran
LONGUEUR = 1280
LARGEUR = 720
screen = pygame.display.set_mode(
    (LONGUEUR, LARGEUR)
)  # Variable globale :/   TODO Faire que ça ne soit pas une variable globale
pygame.display.set_caption("Filosofight")
pygame.display.set_icon(pygame.image.load("./icon.png"))

# Timer et fonctionnement du jeu
clock = pygame.time.Clock()
running = True
delta_t = 0.0
game_over = False
gagnant = ""


# Création de l'élève et du prof
prof = Prof(500, (LONGUEUR // 2, LARGEUR // 4), 132, 132)
eleve = Eleve(200, (LONGUEUR // 2, (LARGEUR // 4) * 3), 81, 136)

# Boucle principale
while running:
    # Boucle des évènements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game_over = prof.est_mort()[0] or eleve.est_mort()[0]
    if game_over:
        gagnant = prof.est_mort()[1]
        running = False

    # On remplit l'écran avec le fond d'écran pour tout effacer
    screen.fill("black")

    # Affichage des images (joueurs)
    prof.draw()
    eleve.draw()

    # Mouvement des images (joueurs)
    prof.movement(delta_t)
    eleve.movement(delta_t)

    # Gestion des attaques & collisions
    prof.attack_management()
    eleve.attack_management()

    # Dans l'ordre: Affichage, mouvement, puis collisions des attaques du Prof et de l'Eleve (+ fonctionnement des Tables)
    for object in prof.get_current_attacks():
        object.draw()
        object.movement(delta_t)
        object.collisions(
            eleve, eleve.get_current_tables()
        )  # Collisions des attaques du prof avec l'élève
    for object in eleve.get_current_attacks():
        object.draw()
        object.movement(delta_t)
        object.collisions(
            prof, eleve.get_current_tables()
        )  # Collisions des attaques de l'élève avec le prof
    for object in eleve.get_current_tables():
        object.draw()

    # Gestion des objets déchets à supprimer
    # Pour le Prof
    for object_index in range(len(prof.get_current_attacks())):
        try:
            prof.get_current_attacks()[object_index].supprimer_dechets(
                prof.get_current_attacks(), object_index
            )
        except:
            pass  # La suppression essaye parfois de supprimer un objet en dehors de la liste. Pour contrer le problème, on saute une frame pour supprimer l'objet à la frame suivante.
    # Pour l'Eleve - Attaques
    for object_index in range(len(eleve.get_current_attacks())):
        try:
            eleve.get_current_attacks()[object_index].supprimer_dechets(
                eleve.get_current_attacks(), object_index
            )
        except:
            pass  # La suppression essaye parfois de supprimer un objet en dehors de la liste. Pour contrer le problème, on saute une frame pour supprimer l'objet à la frame suivante.
    # Pour l'Eleve - Tables
    for object_index in range(len(eleve.get_current_tables())):
        try:
            eleve.get_current_tables()[object_index].supprimer_dechets(
                eleve.get_current_tables(), object_index
            )
        except:
            pass  # La suppression essaye parfois de supprimer un objet en dehors de la liste. Pour contrer le problème, on saute une frame pour supprimer l'objet à la frame suivante.

    # Affichage HUD (Affichage Tête-Haute)
    prof.affiche_hud()
    eleve.affiche_hud()

    # flip() met à jour l'écran après l'affichage des images
    pygame.display.flip()

    # Delta t est le temps écoulé depuis la dernière frame
    delta_t = clock.tick(60) / 1000


pygame.quit()
