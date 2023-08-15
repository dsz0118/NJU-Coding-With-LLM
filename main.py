import pygame
import random
from player.Player import Player
from bullet.Bullet import Bullet
from enemy.Enemy import Enemy
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*iCCP: known incorrect sRGB profile.*")

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

# 创建玩家对象
player = Player(WIDTH // 2, HEIGHT - 10)

# 创建子弹和敌机列表
bullets = []
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
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # 控制子弹发射
    if keys[pygame.K_SPACE]:
        player.shoot(bullets)

    # 移动子弹
    for bullet in bullets:
        if bullet.move():
            bullets.remove(bullet)

    # 生成敌机
    enemy = Enemy.spawn()
    if enemy:
        enemies.append(enemy)

    # 移动子弹
    for bullet in bullets:
        bullet.move()
        if bullet.rect.y < 0:
            bullets.remove(bullet)

    # 移动敌机
    for enemy in enemies:
        enemy.move()
        if enemy.rect.y > HEIGHT:
            enemies.remove(enemy)

    # 碰撞检测
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            running = False
        for bullet in bullets:
            if bullet.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                bullets.remove(bullet)

    # 绘制游戏元素
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)

    # 刷新画面
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 游戏结束
pygame.quit()
