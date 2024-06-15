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
GREEN = (0, 255, 0)

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
charge_speed = 0.5  # 電荷の移動速度を遅く設定

# 蓄積された電荷のリスト
plate1_charges = []  # 正に帯電する金属板（上側）
plate2_charges = []  # 負に帯電する金属板（下側）

# 絶縁体内の電子の位置
polarization_arrows = []

# 絶縁体内の矢印の初期化
arrow_count = 40  # 矢印の数を増やして密度を上げる
arrow_length = 20
for i in range(arrow_count):
    x = width // 2 - plate_width // 2 + i * (plate_width // arrow_count)
    polarization_arrows.append([x, height // 2, x, height // 2])

# 金属板内の電子の初期化
plate1_electrons = [[x, plate1_pos[1] + plate_height // 2] for x in range(plate1_pos[0], plate1_pos[0] + plate_width, plate_width // num_charges)]
plate2_electrons = [[x, plate2_pos[1] + plate_height // 2] for x in range(plate2_pos[0], plate2_pos[0] + plate_width, plate_width // num_charges)]

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

    # 金属板内の電子の動きの描画（上側金属板）
    for electron in plate1_electrons:
        if len(plate1_charges) > 0 and electron[1] > plate1_pos[1]:
            electron[1] -= charge_speed / 2  # 電子が上に移動
        pygame.draw.circle(screen, RED, electron, charge_radius // 2)
    
    # 金属板内の電子の動きの描画（下側金属板）
    for electron in plate2_electrons:
        if len(plate2_charges) > 0 and electron[1] < plate2_pos[1] + plate_height:
            electron[1] += charge_speed / 2  # 電子が下に移動
        pygame.draw.circle(screen, BLUE, electron, charge_radius // 2)

    # 絶縁体内の電子の動き（分極）の描画
    for arrow in polarization_arrows:
        # 矢印を更新（分極のシミュレーション）
        if len(plate1_charges) > 0 and arrow[3] > height // 2 - arrow_length:
            arrow[3] -= charge_speed / 10  # 上方向に移動
        elif len(plate1_charges) == 0 and arrow[3] < height // 2:
            arrow[3] += charge_speed / 10  # 元の位置に戻る
        pygame.draw.line(screen, GREEN, (arrow[0], arrow[1]), (arrow[2], arrow[3]), 2)

    # 画面の更新
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
