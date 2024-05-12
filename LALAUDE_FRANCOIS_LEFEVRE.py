# coding : UTF-8

"""
Ce programme créé un jeu pygame dans lequel le personnage doit de défendre
contre des ennemis en lançant des projectiles avant de se faire tuer.

Authors : Martin LALAUDE, Valentine FRANCOIS, Pierrick LEFEVRE
Version : v_4
URL Github : 

"""
import pygame
import math
import random
pygame.init()

class Game:
    def __init__(self):
        self.jeu_demarre = False
        self.all_players = pygame.sprite.Group()
        self.player = player(self)
        self.all_players.add(self.player)
        self.tous_les_ennemis = pygame.sprite.Group()
        self.pressed = {}

    def start(self):
        self.jeu_demarre = True
        self.spawn_monster()
        self.spawn_monster()

    def game_over(self):
        self.tous_les_ennemis = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.jeu_demarre = False
    def update(self, surface):
        surface.blit(self.player.image, self.player.rect)

        self.player.barre_de_vie(surface)

        for projectile in self.player.all_projectiles:
            projectile.move()

        for ennemis in self.tous_les_ennemis:
            ennemis.forward()
            ennemis.barre_de_vie(surface)

        self.player.all_projectiles.draw(surface)

        self.tous_les_ennemis.draw(surface)

        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < surface.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
    def spawn_monster(self):
        ennemi = Ennemis(self)
        self.tous_les_ennemis.add(ennemi)
        
class player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 200
        self.max_health = 200
        self.attack = 10
        self.velocity = 2
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('protagoniste.png')
        self.image = pygame.transform.scale(self.image, (225, 235))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 270

    def damage(self, amount):
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

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))
    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 7
        self.player = player
        self.image = pygame.image.load('projectil.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        self.angle += 4
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    def remove(self):
        self.player.all_projectiles.remove(self)
    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        for monster in self.player.game.check_collision(self, self.player.game.tous_les_ennemis):
            self.remove()
            monster.damage(self.player.attack)
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

    def damage(self, amount):
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
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)


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
                game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.start()
