import pygame
from constants import HEIGHT, WIDTH
class Bullet:
    def __init__(self, x, y, color, bullet_type):
        self.image = pygame.image.load("images/bullet1.png").convert_alpha()  # 根据实际文件路径调整
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.type = bullet_type
        self.image.set_colorkey((255, 255, 255))  # 设置白色为透明
        self.image = self.image.convert_alpha()  # 转换为带透明度的图像
        bullet_size = self.image.get_size()
        change = True
        for y in range(bullet_size[1]):
            for x in range(bullet_size[0]):
                r, g, b, a = self.image.get_at((x, y))
                if a > 0:  # 非透明像素
                    if change:
                        self.image.set_at((x, y), self.color)
                        change = False
                    else:
                        change = True
        self.mask = pygame.mask.from_surface(self.image)

    def move_up(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            return True
        return False

    def mov_down(self):
        self.rect.y += 10
        if self.rect.y > HEIGHT:
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)