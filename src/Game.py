"""
This is a basic puzzle/platform game made to learn the python langauge
"""
import pygame
from queue import Queue
from pygame import *

pygame.init()
DISPLAY_SCALE = 1
DISPLAY_WIDTH = 800 * DISPLAY_SCALE
DISPLAY_HEIGHT = 600 * DISPLAY_SCALE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Title')
GAME_CLOCK = pygame.time.Clock()


class Player(pygame.sprite.Sprite):

    def __init__(self, x_location, y_location, tiles, lives):
        super().__init__()

        self.image = pygame.image.load('images/CharacterSprite.png').convert_alpha()
        self.x_change = 0
        self.y_change = 0
        self.rect = Rect(x_location, y_location, 32, 32)
        self.jump_legal = True
        self.tiles = tiles
        self.mask = pygame.mask.from_surface(self.image)
        self.level_complete = False
        self.lives = lives
        self.is_dead = False

    def gain_lives(self):
        self.lives += 1

    def die(self):
        self.lives -= 1

    def jump(self):

        if self.jump_legal is True:
            self.y_change = -4.5
            self.jump_legal = False

    def collision_detection_x(self, x_change, tiles):
        # Checks for Entitys for the player to collide with

        for t in tiles:
            if pygame.sprite.collide_rect(self, t):
                while pygame.sprite.collide_mask(self, t) is not None:

                    if isinstance(t, Platform):

                        if x_change > 0:
                            self.rect.left += -1

                        if x_change < 0:
                            self.rect.left += 1

                    if isinstance(t, Box):

                        t.x_change = self.x_change
                        # this function checks if the box collides with another object
                        if self.jump_legal is True:
                            if t.box_collision_x(tiles) is False:

                                if x_change > 0:
                                    self.rect.left += -1

                                if x_change < 0:
                                    self.rect.left += 1

                                t.update()
                        else:
                            t.x_change = 0
                            if x_change > 0:
                                self.rect.left += -1

                            if x_change < 0:
                                self.rect.left += 1


    def collision_detection_y(self, y_change, tiles):
        # collides the player while he is moving in the y direction

        for t in tiles:
            if pygame.sprite.collide_rect(self, t):
                if pygame.sprite.collide_mask(self, t) is not None:
                    if isinstance(t, Platform):
                        if y_change > 0:
                            self.rect.bottom = t.rect.top
                            self.jump_legal = True
                            self.y_change = 0

                        if y_change < 0:
                            while pygame.sprite.collide_mask(self, t) is not None:
                                self.rect.top += 1
                                self.y_change = 0

                    if isinstance(t, Box):
                        if y_change > 0:
                            self.rect.bottom = t.rect.top
                            self.jump_legal = True
                            self.y_change = 0

                        if y_change < 0:
                            self.rect.top = t.rect.bottom
                            self.y_change = 0

                    if isinstance(t, Teleporter):
                        self.level_complete = True

                    if isinstance(t, Spike):
                        self.die()
                        self.is_dead = True

    def go_left(self):
        self.x_change = -3

    def go_right(self):
        self.x_change = 3

    def stop(self):
        self.x_change = 0

    def gravity(self):
        self.y_change += .15

    def update(self):

        self.gravity()
        self.rect.left += self.x_change
        self.collision_detection_x(self.x_change, self.tiles)
        self.rect.top += self.y_change
        self.collision_detection_y(self.y_change, self.tiles)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/PlatformEX.png').convert_alpha()
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/Spike.png').convert_alpha()
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Teleporter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/Teleporter.png').convert_alpha()
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/Box.png').convert_alpha()
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_change = 0
        self.y_change = 0
        self.tiles = []

    def update(self):
        self.gravity()
        self.rect.left += self.x_change
        self.box_collision_x(self.tiles)
        self.x_change = 0
        self.rect.bottom += self.y_change
        self.box_collision_y(self.tiles)

    def tile_adder(self, tiles):
        self.tiles = tiles

    def gravity(self):
        self.y_change += .15

    def box_collision_x(self, tiles):
        for t in tiles:
            if t is not self:
                if pygame.sprite.collide_rect(self, t):
                    if pygame.sprite.collide_mask(self, t) is not None:
                        if self.x_change > 0:
                            while pygame.sprite.collide_mask(self, t) is not None:
                                self.rect.left += -1

                        if self.x_change < 0:
                            while pygame.sprite.collide_mask(self, t) is not None:
                                self.rect.left += 1

                        return True
        return False

    def box_collision_y(self, tiles):
        for t in tiles:
            if t is not self:
                if pygame.sprite.collide_rect(self, t):
                    if pygame.sprite.collide_mask(self, t) is not None:
                        if self.y_change > 0:
                            self.rect.bottom = t.rect.top
                            self.y_change = 0


# This is a class of constants, namely the array representations of all of the levels
class Levels():
    def __init__(self):
        super().__init__()
        # this level should never actually be called, merely a blank slate to build more levels
        self.level_template = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "",
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"]
        self.level_1 = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P          B            P",
            "P      PPPPP  PP   PPPPPP",
            "PPPPPP     P  PPPP      P",
            "P          P  P         P",
            "P      PPPPP  PP   PPPPPPP",
            "P          P  PPP       P",
            "PPPPPP     P  PPPP      P",
            "P          P  PPPPP P   P",
            "P      PPPPP  P        PP",
            "P          P  P       PPP",
            "PPPPPP     P  PP     PPPP",
            "P          P  P      P TP",
            "P      PPPPP        PP  P",
            "P          P         P  P",
            "PPPP  P    P  PPPPPPPP  P",
            "P   B P                 P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "",
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"]
        self.level_4 = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P   PPPPPPPPPPPPPPPPPPP P",
            "P                     p P",
            "PPPP    P             P P",
            "P       P             P P",
            "P   PPPPP             P P",
            "P       P             P P",
            "PP      P        B    P P",
            "P P     P        PPP  P P",
            "P       P     B       P P",
            "P       B     PPPP    P P",
            "PPPPPPPPP  B          P P",
            "P          PPPP       P P",
            "P         B           P P",
            "P    B  B P    B   B  P P",
            "P  PPPPPP PPPPPPPPPPPPP P",
            "P B B     PT            P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "",
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"]
        self.level_3 = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P                      TP",
            "P      PPPPPPPPPPPPPPPPPP",
            "P     P                 P",
            "P         B             P",
            "PP      PPPP            P",
            "P                       P",
            "P            P          P",
            "P     B                 P",
            "P    PPP    P           P",
            "P   P                   P",
            "PP       P              P",
            "P                       P",
            "PPP                     P",
            "P                       P",
            "P        B              P",
            "P       PPP             P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "",
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"]
        self.level_2 = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P                       P",
            "P                   P   P",
            "P                       P",
            "P       B  B          B P",
            "P    PPPPPPPPPPPP     PPP",
            "P   P           P      TP",
            "P               P     PPP",
            "PP             P        P",
            "P              P        P",
            "P   P          P        P",
            "P              PPPPPPPP P",
            "PP                      P",
            "P                       P",
            "P   P                   P",
            "P                       P",
            "PP                      P",
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "",
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"]
        self.level_5 = [
            "PPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P                       P",
            "P            P          P",
            "P     P                 P",
            "PP                      P",
            "P                   T   P",
            "PPPPPPPPPP         PPPPPP",
            "",
            "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"]


    # this function returns a queue of all game levels
    def level_queue(self):
        level_queue = Queue(maxsize=100)
        level_queue.put(self.level_1)
        level_queue.put(self.level_2)
        level_queue.put(self.level_3)
        level_queue.put(self.level_4)
        level_queue.put(self.level_5)
        return level_queue


class Level():
    def __init__(self):
        super().__init__()

    def build_level(self, level):
        entities = pygame.sprite.Group()
        tiles = []
        x = y = 0
        current_level = level
        # build the level
        for row in current_level:
            for col in row:
                if col == "P":
                    p = Platform(x, y)
                    tiles.append(p)
                    entities.add(p)
                if col == "S":
                    s = Spike(x, y)
                    tiles.append(s)
                    entities.add(s)
                if col == "T":
                    t = Teleporter(x, y)
                    tiles.append(t)
                    entities.add(t)
                if col == "B":
                    b = Box(x, y)
                    tiles.append(b)
                    entities.add(b)
                x += 32
            y += 32
            x = 0
        # adds reference to the entities for box
        for entity in entities:
            if isinstance(entity, Box):
                entity.tile_adder(entities)
        return entities


def gameloop():
# Initializes game loop with level and player start locations
    end = False
    level_queue = Levels().level_queue()
    current_level = level_queue.get()
    tiles = Level().build_level(current_level)
    x = (DISPLAY_WIDTH * 0.12)
    y = (DISPLAY_HEIGHT * 0.9)
    player = Player(x, y, tiles, 3)

    while not end:
        # starts a new level if the player has completed the current level
        if player.level_complete is True:
            if not level_queue.empty():
                current_level = level_queue.get()
                tiles = Level().build_level(current_level)
                player = Player(x, y, tiles, player.lives)
            else:
                end = True
        if player.is_dead is True:
            if player.lives > 0:
                tiles = Level().build_level(current_level)
                player = Player(x, y, tiles, player.lives)
            else:
                display_message("game over")
                end = True

        GAME_DISPLAY.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_z:
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_p:
                    display_message("paused")
                elif event.key == pygame.K_r:
                    tiles = Level().build_level(current_level)
                    player = Player(x, y, tiles, player.lives)

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:
                    player.stop()
                elif event.key == pygame.K_RIGHT:
                    player.stop()
        player.update()
        for tile in tiles:
            tile.update()
            GAME_DISPLAY.blit(tile.image, (tile.rect.left, tile.rect.top))

        GAME_DISPLAY.blit(player.image, (player.rect.left, player.rect.top))
        pygame.display.flip()
        GAME_CLOCK.tick(60)


def display_message(message):

    base_font = pygame.font.SysFont("arial", 48)
    open = True
    while open:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                open = False

        GAME_DISPLAY.fill(WHITE)
        text_surf = base_font.render(message, True, BLACK)
        GAME_DISPLAY.blit(text_surf, ((DISPLAY_WIDTH / 2) - 335, (DISPLAY_HEIGHT / 2)))
        pygame.display.update()
        GAME_CLOCK.tick(60)


display_message("Click Anywhere to Start Game")
gameloop()
display_message("THE END")
pygame.quit()
quit()
