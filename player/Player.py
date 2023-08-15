import pygame
from bullet.Bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/me1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.bullet_delay = 300  # 子弹发射间隔（毫秒）
        self.last_bullet_time = 0

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5

    def shoot(self, bullets):
        current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）
        if current_time - self.last_bullet_time > self.bullet_delay:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.append(bullet)
            self.last_bullet_time = current_time  # 更新上一次发射时间
