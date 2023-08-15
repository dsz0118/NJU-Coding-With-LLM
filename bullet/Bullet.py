import pygame

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)

    def move(self):
        self.rect.y -= 10
