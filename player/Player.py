import pygame
from bullet.Bullet import Bullet
from animation.Animation import PlaneDestroyAnimation

class Player:
    def __init__(self, x, y):
        # 初始化飞机属性
        self.image = pygame.image.load("images/me1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.destroy_images = [pygame.image.load("images/me_destroy_1.png"),
                               pygame.image.load("images/me_destroy_2.png"),
                               pygame.image.load("images/me_destroy_3.png"),
                               pygame.image.load("images/me_destroy_4.png")]

        # 初始化其他属性
        self.speed = 5
        self.bullets = []
        self.destroyed = False
        self.destroy_animation = None
        self.bullets_paused = False  # 添加属性用于暂停子弹
        self.enemies_paused = False  # 添加属性用于暂停敌方飞机
        self.score = 0  # 添加 score 属性并初始化为零

        # 子弹发射间隔（毫秒）
        self.bullet_delay = 300
        self.last_bullet_time = 0

    def restart_game(self):
        self.speed = 5
        self.bullets = []
        self.destroyed = False
        self.destroy_animation = None
        self.bullets_paused = False
        self.enemies_paused = False
        self.score = 0

        # 子弹发射间隔（毫秒）
        self.bullet_delay = 300
        self.last_bullet_time = 0

    def update(self):
        # 更新飞机位置
        if not self.destroyed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.move_left()
            if keys[pygame.K_RIGHT]:
                self.move_right()

        # 更新子弹位置
        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 更新撞毁动画
        if self.destroyed and self.destroy_animation:
            self.destroy_animation.update()

    def draw(self, screen):
        # 绘制飞机
        if not self.destroyed:
            screen.blit(self.image, self.rect)

        # 绘制子弹
        for bullet in self.bullets:
            screen.blit(bullet.image, bullet.rect)

        # 绘制撞毁动画
        if self.destroyed and self.destroy_animation:
            screen.blit(self.destroy_animation.image, self.destroy_animation.rect)

    def collide_with_enemy(self, enemies):
        if not self.destroyed:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    self.destroyed = True
                    self.destroy_animation = PlaneDestroyAnimation(self.rect.centerx, self.rect.centery, self.destroy_images)
                    self.pause_bullets_and_enemies()
                    return  # 退出碰撞检测

    def is_destroyed(self):
        return self.destroyed and self.destroy_animation.frame == len(self.destroy_animation.images) - 1

    def pause_bullets_and_enemies(self):
        self.bullets_paused = True
        self.enemies_paused = True

    def resume_bullets_and_enemies(self):
        self.bullets_paused = False
        self.enemies_paused = False

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5

    def move_up(self):
        self.rect.y -= 5

    def move_down(self):
        self.rect.y += 5

    def shoot(self, bullets):
        current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）
        if current_time - self.last_bullet_time > self.bullet_delay:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.append(bullet)
            self.last_bullet_time = current_time  # 更新上一次发射时间
