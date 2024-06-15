import pygame
import sys

# 初期設定
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("コンデンサ充電シミュレーション")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# コンデンサの位置とサイズ
plate_width, plate_height = 200, 20
plate1_pos = (width // 2 - plate_width // 2, height // 3)
plate2_pos = (width // 2 - plate_width // 2, height // 3 * 2)

# 電荷の初期状態
charges = []
charge_radius = 5
num_charges = 50

# 電荷の生成
for i in range(num_charges):
    x = width // 2 - plate_width // 2 + i * (plate_width // num_charges)
    charges.append([x, plate2_pos[1] + plate_height // 2])

# メインループ
running = True
clock = pygame.time.Clock()
charge_speed = 1  # 電荷の移動速度

# 蓄積された電荷のリスト
plate1_charges = []  # 正に帯電する金属板（上側）
plate2_charges = []  # 負に帯電する金属板（下側）

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 背景の描画
    screen.fill(WHITE)
    
    # コンデンサの金属板の描画
    pygame.draw.rect(screen, BLACK, (*plate1_pos, plate_width, plate_height))
    pygame.draw.rect(screen, BLACK, (*plate2_pos, plate_width, plate_height))
    
    # 電荷の移動と描画
    for charge in charges:
        if charge[1] > plate1_pos[1] + plate_height // 2:
            charge[1] -= charge_speed
        else:
            # 電荷が上側の金属板に到達したら、蓄積された電荷リストに追加
            if charge not in plate1_charges:
                plate1_charges.append(charge)
                # 下側の金属板にも対応する電荷を追加
                plate2_charges.append([charge[0], plate2_pos[1] + plate_height // 2])
    
    # 蓄積された電荷の描画（正に帯電する金属板）
    for charge in plate1_charges:
        pygame.draw.circle(screen, RED, charge, charge_radius)
    
    # 蓄積された電荷の描画（負に帯電する金属板）
    for charge in plate2_charges:
        pygame.draw.circle(screen, BLUE, charge, charge_radius)

    # 画面の更新
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
