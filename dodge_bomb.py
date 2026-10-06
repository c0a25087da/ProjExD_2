import os
import pygame as pg
import random
import sys
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0, -5), pg.K_DOWN:(0, +5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(+5, 0)}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんまたは爆弾のRect
    戻り値：タプル（横方向の判定結果, 縦方向の判定結果）
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数：バックグラウンド背景
    戻り値：なし
    ゲームオーバー画面の作成
    """
    go_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(100)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, [400, 300])
    kk_img = pg.image.load("fig/8.png")
    screen.blit(kk_img, [200, 300])
    screen.blit(kk_img, [800, 300])
    screen.blit(go_img, [0,0])
    pg.display.update()
    time.sleep(5)


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数：なし
    戻り値：rotozoomしたSurfaceを値とした辞書を返す
    こうかとんの移動に伴った画像切り替え
    """
    kk_img = pg.image.load("fig/3.png") 
    kk_reverse = pg.transform.flip(kk_img, True, False) 
    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (+5, 0): pg.transform.rotozoom(kk_reverse, 0, 1.0),
        (+5, -5):pg.transform.rotozoom(kk_reverse, 45, 1.0),
        (0, -5):pg.transform.rotozoom(kk_reverse, 90, 1.0),
        (+5, +5):pg.transform.rotozoom(kk_reverse, -45, 1.0),
        (0, +5):pg.transform.rotozoom(kk_reverse, -90, 1.0),
        (-5, 0):pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, -5):pg.transform.rotozoom(kk_img, -45, 1.0),
        (-5, +5):pg.transform.rotozoom(kk_img, 45, 1.0),
    }
    
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_imgs = get_kk_imgs()
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  # 赤い爆弾の四隅を透過
    bb_rct = bb_img.get_rect()  # 爆弾のRCT
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  #横座標と縦座標の乱数
    vx, vy = +5, +5  # 赤い爆弾の移動量  
    
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        
        if kk_rct.colliderect(bb_rct):  # kkとbbのrectが重なっていたら
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向の移動量
                sum_mv[1] += tpl[1]  # 縦方向の移動量
                
        kk_img = kk_imgs[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # どこかしらはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 先ほどの動きをキャンセルする
        screen.blit(kk_img, kk_rct)
        
        bb_rct.move_ip(vx, vy)  # 赤い爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習2赤い爆弾の表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
