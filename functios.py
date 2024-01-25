import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

class Game:
    def __init__(self):
        pygame.init()

        self.FPS = pygame.time.Clock()

        self.HEIGHT = 800
        self.WIDTH = 1200

        self.FONT = pygame.font.SysFont('Verdana', 20)

        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_BLUE = (0, 0, 255)
        self.COLOR_GREEN = (0, 255, 0)

        self.main_display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.background = pygame.transform.scale(pygame.image.load('background.png'), (self.WIDTH, self.HEIGHT))
        self.background_x1 = 0
        self.background_x2 = self.background.get_width()
        self.background_move = 3

        self.IMAGE_PATH = "Goose_animation"
        self.PLAYER_IMAGES = os.listdir(self.IMAGE_PATH)

        self.player_size = (20, 20)
        self.player = pygame.image.load('player.png').convert_alpha()
        self.player_rect = self.player.get_rect()
        self.player_rect.center = self.main_display.get_rect().center
        self.player_move_down = [0, 4]
        self.player_move_up = [0, -4]
        self.player_move_right = [4, 0]
        self.player_move_left = [-4, 0]

        self.enemies = []
        self.bonuses = []

        self.CREATE_BONUS = pygame.USEREVENT + 2
        pygame.time.set_timer(self.CREATE_BONUS, 3000)

        self.CREATE_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.CREATE_ENEMY, 1500)

        self.CHANGE_IMAGE = pygame.USEREVENT + 3
        pygame.time.set_timer(self.CHANGE_IMAGE, 200)

        self.score = 0
        self.image_index = 0

    def create_enemy(self):
        enemy = pygame.image.load('enemy.png').convert_alpha()
        enemy_rect = pygame.Rect(self.WIDTH, random.randint(enemy.get_height(), self.HEIGHT - enemy.get_height()),
                                 *enemy.get_size())
        enemy_move = [random.randint(-8, -4), 0]
        return [enemy, enemy_rect, enemy_move]

    def create_bonus(self):
        bonus_size = (30, 30)
        bonus = pygame.image.load('bonus.png').convert_alpha()
        bonus_width = bonus.get_width()
        bonus_rect = pygame.Rect(random.randint(bonus_width, self.WIDTH - bonus_width), -bonus.get_height(),
                                 *bonus.get_size())
        bonus_move = [0, random.randint(4, 8)]
        return [bonus, bonus_rect, bonus_move]

    def run(self):
        playing = True
        while playing:
            self.FPS.tick(660)

            for event in pygame.event.get():
                if event.type == QUIT:
                    playing = False
                if event.type == self.CREATE_ENEMY:
                    self.enemies.append(self.create_enemy())
                if event.type == self.CREATE_BONUS:
                    self.bonuses.append(self.create_bonus())
                if event.type == self.CHANGE_IMAGE:
                    self.player = pygame.image.load(os.path.join(self.IMAGE_PATH, self.PLAYER_IMAGES[self.image_index]))
                    self.image_index += 1
                    if self.image_index >= len(self.PLAYER_IMAGES):
                        self.image_index = 0

            self.background_x1 -= self.background_move
            self.background_x2 -= self.background_move

            if self.background_x1 < -self.background.get_width():
                self.background_x1 = self.background.get_width()

            if self.background_x2 < -self.background.get_width():
                self.background_x2 = self.background.get_width()

            self.main_display.blit(self.background, (self.background_x1, 0))
            self.main_display.blit(self.background, (self.background_x2, 0))

            keys = pygame.key.get_pressed()

            if keys[K_DOWN] and self.player_rect.bottom < self.HEIGHT:
                self.player_rect = self.player_rect.move(self.player_move_down)

            if keys[K_UP] and self.player_rect.top >= 0:
                self.player_rect = self.player_rect.move(self.player_move_up)

            if keys[K_RIGHT] and self.player_rect.right < self.WIDTH:
                self.player_rect = self.player_rect.move(self.player_move_right)

            if keys[K_LEFT] and self.player_rect.left >= 0:
                self.player_rect = self.player_rect.move(self.player_move_left)

            for enemy in self.enemies:
                enemy[1] = enemy[1].move(enemy[2])
                self.main_display.blit(enemy[0], enemy[1])

                if self.player_rect.colliderect(enemy[1]):
                    playing = False

            for bonus in self.bonuses:
                bonus[1] = bonus[1].move(bonus[2])
                self.main_display.blit(bonus[0], bonus[1])

                if self.player_rect.colliderect(bonus[1]):
                    self.score += 1
                    self.bonuses.pop(self.bonuses.index(bonus))

            self.main_display.blit(self.FONT.render(str(self.score), True, self.COLOR_BLACK), (self.WIDTH - 50, 20))

            self.main_display.blit(self.player, self.player_rect)

            pygame.display.flip()

            for enemy in self.enemies:
                if enemy[1].right < 0:
                    self.enemies.pop(self.enemies.index(enemy))

            for bonus in self.bonuses:
                if bonus[1].top > self.HEIGHT:
                    self.bonuses.pop(self.bonuses.index(bonus))