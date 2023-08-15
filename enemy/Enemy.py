import pygame
import random

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/enemy1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.y += 5

    @staticmethod
    def spawn():
        if random.randint(0, 100) < 2:
            return Enemy(random.randint(0, 800), 0)
        return None
