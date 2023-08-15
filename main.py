import pygame
import random
from player.Player import Player
from bullet.Bullet import Bullet
from enemy.Enemy import Enemy


# 初始化
pygame.init()

# 游戏窗口大小
WIDTH = 800
HEIGHT = 600

# 颜色定义
WHITE = (255, 255, 255)

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("飞机大战")

# 加载暂停界面图像
pause_image = pygame.image.load("images/pause_nor.png")
pause_rect = pause_image.get_rect()
pause_rect.center = (WIDTH // 2, HEIGHT // 2)


# 创建玩家对象
player = Player(WIDTH // 2, HEIGHT - 10)

# 创建子弹和敌机列表
bullets = []
enemies = []


# 游戏时钟
clock = pygame.time.Clock()

# 暂停标志
paused = False

# 主游戏循环
running = True


while running:

    # 运行状态判断
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if paused:
                    running = False
                else:
                    paused = True
            else:
                paused = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if paused:
                paused = False

    # 未暂停
    if not paused:
        # 控制飞机移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()

        # 控制子弹发射
        if keys[pygame.K_SPACE] and not player.bullets_paused:
            player.shoot(bullets)

        # 生成敌机
        enemy = Enemy.spawn()
        if enemy and not player.enemies_paused:
            enemies.append(enemy)

        # # 碰撞检测
        # for enemy in enemies:
        #     # # 检查撞毁动画是否播放完毕
        #     # if player.destroyed and player.destroy_animation_finished:
        #     #     running = False  # 结束游戏
        #     for bullet in bullets:
        #         if bullet.rect.colliderect(enemy.rect):
        #             enemies.remove(enemy)
        #             bullets.remove(bullet)

    # 绘制游戏元素
    screen.fill(WHITE)

    if paused:
        screen.blit(pause_image, pause_rect)
    else:
        player.update()
        player.draw(screen)

        # 移动子弹
        for bullet in bullets:
            if not player.bullets_paused:
                bullet.move()
            if bullet.rect.y < 0:
                bullets.remove(bullet)
            screen.blit(bullet.image, bullet.rect)

        # 移动敌机
        for enemy in enemies:
            if not player.enemies_paused:
                enemy.move()
            if enemy.rect.y > HEIGHT:
                enemies.remove(enemy)
            screen.blit(enemy.image, enemy.rect)

        player.collide_with_enemy(enemies)  # 检测碰撞

        # 检查飞机是否被摧毁
        if player.is_destroyed():
            running = False  # 结束游戏

    # 刷新画面
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 游戏结束
pygame.quit()
