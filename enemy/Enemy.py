import pygame
import random
from bullet.Bullet import Bullet

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "enemy"
        # 子弹发射间隔（毫秒）
        self.bullet_delay = 300
        self.last_bullet_time = 0

    def move(self):
        self.rect.y += 5

    @staticmethod
    def spawn(spawn_rate):
        if random.randint(0, 1000) + spawn_rate * 1000 > 990:
            return Enemy(random.randint(0, 800), 0)
        return None

    def shoot(self, bullets):
        current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）
        if current_time - self.last_bullet_time > self.bullet_delay:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, (255, 0, 0), self.type)  # 创建红色子弹
            bullets.append(bullet)
            self.last_bullet_time = current_time  # 更新上一次发射时间
