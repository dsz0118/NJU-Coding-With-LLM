import pygame
import random
from player.Player import Player
from bullet.Bullet import Bullet
from enemy.Enemy import Enemy
from constants import HEIGHT, WIDTH

# 初始化
pygame.init()

# 加载字体
font = pygame.font.Font(None, 36)



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

        # 检查飞机是否被摧毁
        if player.is_destroyed():

            restart_image = pygame.image.load("images/again.png")
            restart_rect = restart_image.get_rect()
            restart_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(restart_image, restart_rect)
            pygame.display.flip()  # 刷新画面以显示飞机坠毁的画面

            restart = False
            while not restart:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            restart = True
                        else:
                            # 重新开始游戏
                            player = Player(WIDTH // 2, HEIGHT - 10)
                            bullets = []
                            enemies = []
                            restart = True

        else:
            # 控制飞机移动
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_RIGHT]:
                player.move_right()
            if keys[pygame.K_UP]:
                player.move_up()
            if keys[pygame.K_DOWN]:
                player.move_down()

            # 控制子弹发射
            if keys[pygame.K_SPACE] and not player.bullets_paused:
                player.shoot(bullets)

            # 生成敌机
            if len(enemies) < player.max_enemy_numbers():
                spawn_rate, shoot_rate = player.adjust_enemy_rates()
                enemy = Enemy.spawn(spawn_rate)
                if enemy and not player.enemies_paused:
                    enemies.append(enemy)
                    if random.random() < shoot_rate:  # 控制发射子弹的概率，你可以根据需要调整
                        enemy.shoot(bullets)

            # 碰撞检测与操作
            for bullet in bullets:
                for enemy in enemies:
                    if bullet.type == player.type:
                        offset = (enemy.rect.x - bullet.rect.x, enemy.rect.y - bullet.rect.y)
                        if bullet.mask.overlap(enemy.mask, offset):
                            enemies.remove(enemy)
                            bullets.remove(bullet)
                            player.score += 10  # 增加分数

        # 绘制游戏元素
        screen.fill(WHITE)
        player.update()
        player.draw(screen)

        # 移动子弹
        for bullet in bullets:
            if not player.bullets_paused:
                if bullet.type == player.type and bullet.move_up():
                    bullets.remove(bullet)
                if bullet.type != player.type and bullet.mov_down():
                    bullets.remove(bullet)
            # screen.blit(bullet.image, bullet.rect)
            bullet.draw(screen)

        # 移动敌机
        for enemy in enemies:
            if not player.enemies_paused:
                enemy.move()
            if enemy.rect.y > HEIGHT:
                enemies.remove(enemy)
            screen.blit(enemy.image, enemy.rect)

        player.collide_with_enemy(enemies)  # 检测碰撞
        player.collide_with_bullet(bullets)

    else:
        screen.blit(pause_image, pause_rect)

    # 绘制分数文本
    score_text = font.render(f"Score: {player.score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))  # 在居中顶部显示分数

    # 刷新画面
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 游戏结束
pygame.quit()
