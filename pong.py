import math
import random

import pyxel


BLACK = 0
WHITE = 7
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
PADDLE_SIZE = 5
BALL_SIZE = 3
BALL_SPEED = 1
BALL_PARAMS = [
    SCREEN_WIDTH / 2,
    SCREEN_HEIGHT / 2,
    random.choice([-2, 2]),
    random.choice([-2, 2])
]


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Velocity:
    def __init__(self, x, y):
        self.m = math.sqrt(x * x + y * y)
        self.x = x / self.m * BALL_SPEED
        self.y = y / self.m * BALL_SPEED


class HitBox:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Ball:
    def __init__(self, px, py, vx, vy):
        self.pos = Vector(px, py)
        self.vel = Velocity(vx, vy)

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # Collision with walls
        if self.pos.y >= SCREEN_HEIGHT - BALL_SIZE:
            self.vel.y = -self.vel.y
        if self.pos.y <= BALL_SIZE:
            self.vel.y = -self.vel.y

    def bounce(self):
        self.vel.x = -self.vel.x
        self.vel.y = self.vel.y  # + random.uniform(-1.1, 1.1)

    def restart(self):
        self.__init__(*BALL_PARAMS)


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.hitbox = []

    def calculate_hitbox(self):
        self.hitbox.clear()
        for x in range(self.x - 1, self.x + PADDLE_SIZE + 1):
            for y in range(self.y - 1, self.y + PADDLE_SIZE * 5 + 1):
                self.hitbox.append((x, y))


class Pong:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Pong", fps=60, quit_key=pyxel.KEY_ESCAPE)
        self.playing = False
        self.ball = Ball(*BALL_PARAMS)
        self.player_left = Paddle(0, SCREEN_HEIGHT // 2)
        self.player_right = Paddle(SCREEN_WIDTH - 5, SCREEN_HEIGHT // 2)
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.playing and pyxel.btn(pyxel.KEY_ENTER):
            self.playing = True
        elif self.playing:
            self.ball.update()
            self.player_right.calculate_hitbox()
            self.player_left.calculate_hitbox()

            # Paddles Movement
            if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD_1_UP):
                if self.player_left.y > 2:
                    self.player_left.y -= 2
            if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
                if self.player_left.y < 229:
                    self.player_left.y += 2
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_2_UP):
                if self.player_right.y > 2:
                    self.player_right.y -= 2
            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_2_DOWN):
                if self.player_right.y < 229:
                    self.player_right.y += 2

            # Collision with Paddles
            if (int(self.ball.pos.x), int(self.ball.pos.y)) in self.player_right.hitbox:
                self.ball.bounce()
            if (int(self.ball.pos.x), int(self.ball.pos.y)) in self.player_left.hitbox:
                self.ball.bounce()

            # Goal
            if self.ball.pos.x >= SCREEN_WIDTH - BALL_SIZE:
                self.ball.restart()
                self.player_left.score += 1
            if self.ball.pos.x <= BALL_SIZE:
                self.ball.restart()
                self.player_right.score += 1

    def draw(self):
        if self.playing:
            pyxel.cls(BLACK)

            # Ball
            pyxel.circ(self.ball.pos.x, self.ball.pos.y, BALL_SIZE, WHITE)

            # Paddles
            pyxel.rect(
                self.player_left.x,
                self.player_left.y,
                PADDLE_SIZE,
                PADDLE_SIZE * 5,
                WHITE
            )
            pyxel.rect(
                self.player_right.x,
                self.player_right.y,
                PADDLE_SIZE,
                PADDLE_SIZE * 5,
                WHITE
            )

            # Top Bar
            pyxel.line(0, 0, 256, 0, WHITE)
            pyxel.line(0, 1, 256, 1, WHITE)

            # Bottom Bar
            pyxel.line(0, 255, 256, 255, WHITE)
            pyxel.line(0, 254, 256, 254, WHITE)

            # Middle Bar
            pyxel.line(127, 0, 127, 254, WHITE)
            pyxel.line(128, 0, 128, 254, WHITE)

            # Left Score
            pyxel.text(120, 5, str(self.player_left.score), WHITE)

            # Right Score
            pyxel.text(133, 5, str(self.player_right.score), WHITE)
        else:
            pyxel.text(90, 128, "Press ENTER to start", WHITE)


if __name__ == '__main__':
    Pong()
