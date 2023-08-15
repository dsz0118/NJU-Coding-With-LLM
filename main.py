import pygame
import random
from player import Player
from bullet import Bullet
from enemy import Enemy

# 初始化
pygame.init()

# 游戏窗口大小
WIDTH = 800
HEIGHT = 600

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("飞机大战")

# 飞机图片加载
player_img = pygame.image.load("images/me1.png")
player_rect = player_img.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 10

# 子弹图片加载
bullet_img = pygame.image.load("images/bullet1.png")
bullets = []

# 敌机图片加载
enemy_img = pygame.image.load("images/enemy1.png")
enemies = []

# 游戏时钟
clock = pygame.time.Clock()

# 子弹发射间隔控制
bullet_delay = 300  # 子弹发射间隔（毫秒）
last_bullet_time = 0

# 主游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制飞机移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5

    # 控制子弹发射间隔
    current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）
    if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_delay:
        bullet = pygame.Rect(player_rect.centerx, player_rect.top, 5, 10)
        bullets.append(bullet)
        last_bullet_time = current_time  # 更新上一次发射时间

    # 移动子弹
    for bullet in bullets:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)

    # 生成敌机
    if random.randint(0, 100) < 2:
        enemy = pygame.Rect(random.randint(0, WIDTH), 0, 50, 50)
        enemies.append(enemy)

    # 移动敌机
    for enemy in enemies:
        enemy.y += 5
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

    # 碰撞检测
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            running = False
        for bullet in bullets:
            if bullet.colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)

    # 绘制游戏元素
    screen.fill(WHITE)
    screen.blit(player_img, player_rect)
    for bullet in bullets:
        screen.blit(bullet_img, bullet)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    # 刷新画面
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 游戏结束
pygame.quit()
