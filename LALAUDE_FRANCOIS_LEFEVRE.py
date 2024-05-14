# coding : UTF-8

"""
Ce programme créé un jeu pygame dans lequel le personnage doit de défendre
contre des ennemis en lançant des projectiles avant de se faire tuer.

Authors : Martin LALAUDE, Valentine FRANCOIS, Pierrick LEFEVRE
Version : v_4
URL Github : https://github.com/RTxmrt/nsi-fin-annee-final

Nous nous sommes aidés de la video pygame explicative de Graven et des conseils d'un programmeur professionel
Pour les images, nous les avons trouvées sur internet puis nous les avons détourées pour qu'elles correspondent a nos attentes
"""
import pygame
import math
import random
pygame.init()

class Game:
    def __init__(self):
        self.jeu_demarre = False
        self.tout_les_joueurs = pygame.sprite.Group()
        self.joueur = joueur(self)
        self.tout_les_joueurs.add(self.joueur)
        self.tous_les_ennemis = pygame.sprite.Group()
        self.pressed = {}
        self.nb_ennemis_tues = 0

    def start(self):
        self.jeu_demarre = True
        self.spawn_monster()
        self.spawn_monster()

    def game_over(self):
        self.tous_les_ennemis = pygame.sprite.Group()
        self.joueur.health = self.joueur.max_health
        self.jeu_demarre = False
        self.nb_ennemis_tues = 0
        
    def update(self, surface):
        font = pygame.font.SysFont("arial", 26)
        nb_ennemis_tues_affichage = font.render(f"Nombre d'ennemis tués : {self.nb_ennemis_tues}", 1, (250, 250, 250))
        surface.blit(nb_ennemis_tues_affichage, (20, 20))
        surface.blit(self.joueur.image, self.joueur.rect)

        self.joueur.barre_de_vie(surface)

        for projectile in self.joueur.all_projectiles:
            projectile.move()

        for ennemis in self.tous_les_ennemis:
            ennemis.forward()
            ennemis.barre_de_vie(surface)

        self.joueur.all_projectiles.draw(surface)

        self.tous_les_ennemis.draw(surface)

        if self.pressed.get(pygame.K_RIGHT) and self.joueur.rect.x + self.joueur.rect.width < surface.get_width():
            self.joueur.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.joueur.rect.x > 0:
            self.joueur.move_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
    def spawn_monster(self):
        ennemi = Ennemis(self)
        self.tous_les_ennemis.add(ennemi)
        
class joueur(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 200
        self.max_health = 200
        self.attack = 10
        self.velocity = 10
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('protagoniste.png')
        self.image = pygame.transform.scale(self.image, (225, 235))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 270

    def degat(self, amount):
        if self.health - amount > amount:
            self.health -= amount
        else:
            self.game.game_over()
    def barre_de_vie(self, surface):
        couleur_barre_vie = (91, 131, 197)
        fond_barre_vie = (60, 63, 60)
        position_barre = [425, 75, self.health, 20]
        position_barre_fond = [425, 75, self.max_health, 20]
        pygame.draw.rect(surface, fond_barre_vie, position_barre_fond)
        pygame.draw.rect(surface, couleur_barre_vie, position_barre)

    def lancer_de_boules(self):
        self.all_projectiles.add(Projectile(self))
    def move_right(self):
        if not self.game.check_collision(self, self.game.tous_les_ennemis):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity


class Projectile(pygame.sprite.Sprite):
    def __init__(self, joueur):
        super().__init__()
        self.velocity = 7
        self.joueur = joueur
        self.image = pygame.image.load('projectile.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = joueur.rect.x + 120
        self.rect.y = joueur.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        self.angle += 4
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    def remove(self):
        self.joueur.all_projectiles.remove(self)
    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        for monster in self.joueur.game.check_collision(self, self.joueur.game.tous_les_ennemis):
            self.remove()
            monster.degat(self.joueur.attack)
        if self.rect.x > 1080:
            self.remove()

class Ennemis(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.5
        self.image = pygame.image.load('antagoniste.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (400, 400))
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 290
        self.velocity = random.randint(1, 2)

    def degat(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, 3)
            self.health = self.max_health

    def barre_de_vie(self, surface):
        couleur_barre_vie = (133, 91, 197 )
        fond_barre_vie = (60, 63, 60)
        position_barre = [self.rect.x + 230, self.rect.y - 10, self.health, 5]
        position_barre_fond = [self.rect.x + 230, self.rect.y - 10, self.max_health, 5]
        pygame.draw.rect(surface, fond_barre_vie, position_barre_fond)
        pygame.draw.rect(surface, couleur_barre_vie, position_barre)

    def forward(self):
        if not self.game.check_collision(self, self.game.tout_les_joueurs):
            self.rect.x -= self.velocity
        else:
            self.game.joueur.degat(self.attack)


pygame.init()
pygame.display.set_caption("Jeu de combat Pygame")
surface = pygame.display.set_mode((1080, 720))

# chargement arrière plan
arriere_plan = pygame.image.load("arène.jpg")
arriere_plan = pygame.transform.scale(arriere_plan, (1080, 720))

# chargement bannière début

banniere = pygame.image.load("bannière.png")
banniere = pygame.transform.scale(banniere, (1080, 720))
banniere_rect = banniere.get_rect()


play_button = pygame.image.load("bouton play.png")
play_button = pygame.transform.scale(play_button, ((500, 500)))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(surface.get_width() / 3.33)
play_button_rect.y = math.ceil(surface.get_width() / 4)

game = Game()


running = True

while running:

    surface.blit(arriere_plan, (0, 0))

    if game.jeu_demarre:
        game.update(surface)
    else:
        surface.blit(banniere, banniere_rect)
        surface.blit(play_button, play_button_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                game.joueur.lancer_de_boules()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.start()
