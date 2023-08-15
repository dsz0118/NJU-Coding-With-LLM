import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/me1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5
