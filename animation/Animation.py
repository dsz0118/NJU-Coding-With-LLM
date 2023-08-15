import pygame

class PlaneDestroyAnimation:
    def __init__(self, x, y, destroy_images):
        self.images = destroy_images
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = pygame.time.get_ticks()
        self.frame_duration = 500  # 调整帧切换时间间隔

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.timer > self.frame_duration:  # 调整动画帧切换速度
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = len(self.images) - 1
            self.image = self.images[self.frame]
            self.timer = current_time