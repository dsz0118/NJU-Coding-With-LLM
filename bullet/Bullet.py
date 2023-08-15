import pygame

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/bullet1.png")  # 根据实际文件路径调整
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            return True
        else:
            return False