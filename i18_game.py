import pyxel
import random

class JumpGame:
    def __init__(self):
        # 画面サイズ: 幅160, 高さ120
        pyxel.init(160, 120, title="Neon Runner", fps=60)
        
        # ゲーム変数の初期化
        self.reset_game()
        
        # 星（背景）の初期化
        self.stars = [(random.randint(0, 160), random.randint(0, 100), random.randint(1, 3)) for _ in range(20)]

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.is_game_over = False
        self.score = 0
        self.speed = 2.0  # 初期の進行スピード
        
        # プレイヤー設定
        self.player_x = 20
        self.player_y = 100
        self.player_dy = 0
        self.is_jumping = False
        
        # 障害物リスト [(x, y, type)] type 0=small, 1=tall
        self.obstacles = []
        self.spawn_timer = 0

    def update(self):
        # ゲームオーバー時の処理
        if self.is_game_over:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.reset_game()
            return

        # --- プレイヤーの動き ---
        # ジャンプ
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)) and not self.is_jumping:
            self.player_dy = -10  # ジャンプ力
            self.is_jumping = True
        
        # 重力と位置更新
        self.player_dy += 0.8  # 重力
        self.player_y += self.player_dy

        # 地面との当たり判定
        if self.player_y >= 100:
            self.player_y = 100
            self.player_dy = 0
            self.is_jumping = False

        # --- 障害物の生成と移動 ---
        self.spawn_timer -= 1
        if self.spawn_timer < 0:
            # 障害物の種類をランダムに決定
            obs_type = random.randint(0, 1) 
            self.obstacles.append([170, 100, obs_type])
            # 次の出現までの間隔（スピードが速いほど短くなる）
            self.spawn_timer = random.randint(40, 90) - (self.speed * 2)
            if self.spawn_timer < 20: self.spawn_timer = 20

        # 障害物の更新
        for obs in self.obstacles:
            obs[0] -= self.speed
        
        # 画面外に出た障害物を削除
        self.obstacles = [obs for obs in self.obstacles if obs[0] > -20]

        # --- 当たり判定 ---
        player_rect = [self.player_x, self.player_y, 8, 8] # x, y, w, h
        
        for obs in self.obstacles:
            ox = obs[0]
            oy = obs[1]
            otype = obs[2]
            
            # 障害物のサイズ定義
            ow = 8 if otype == 0 else 6
            oh = 8 if otype == 0 else 14
            oy_draw = oy if otype == 0 else oy - 6

            # AABB衝突判定 (Axis-Aligned Bounding Box)
            if (self.player_x < ox + ow and
                self.player_x + 8 > ox and
                self.player_y < oy_draw + oh and
                self.player_y + 8 > oy_draw):
                self.is_game_over = True
                # 衝突時のエフェクト（簡易的に色を変えるなどで表現）
                pyxel.play(0, 0) # 音があれば鳴らす(今回は未定義)

        # --- スコアと難易度 ---
        self.score += 1
        # スコアに応じてスピードアップ（最大スピードを制限）
        if self.score % 300 == 0:
            self.speed = min(self.speed + 0.5, 6.0)

        # --- 背景の更新 ---
        for i, star in enumerate(self.stars):
            self.stars[i] = ((star[0] - star[2] * (self.speed/4)) % 160, star[1], star[2])

    def draw(self):
        pyxel.cls(0)

        # 背景（星）
        for star in self.stars:
            col = 7 if star[2] == 1 else 13
            pyxel.pset(star[0], star[1], col)

        # 地面
        pyxel.line(0, 108, 160, 108, 6)

        if self.is_game_over:
            # ゲームオーバー画面
            pyxel.text(55, 50, "GAME OVER", 8)
            pyxel.text(45, 60, f"SCORE: {self.score}", 7)
            pyxel.text(40, 80, "PRESS SPACE", 10)
        else:
            # プレイヤー (四角形)
            # ジャンプ中は色を変えて視認性を上げる
            color = 11 if self.is_jumping else 9
            pyxel.rect(self.player_x, self.player_y, 8, 8, color)
            # ちょっとした装飾（目）
            pyxel.pset(self.player_x + 6, self.player_y + 2, 7)

            # 障害物
            for obs in self.obstacles:
                ox = obs[0]
                otype = obs[2]
                if otype == 0:
                    # 小さい障害物
                    pyxel.rect(ox, 100, 8, 8, 8)
                    pyxel.rectb(ox, 100, 8, 8, 2) # 縁取り
                else:
                    # 背の高い障害物
                    pyxel.rect(ox, 94, 6, 14, 14)
                    pyxel.rectb(ox, 94, 6, 14, 4)

            # HUD (スコア)
            pyxel.text(5, 5, f"SCORE: {self.score}", 7)
            pyxel.text(120, 5, f"SPD: {self.speed:.1f}", 6)

JumpGame()