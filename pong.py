import math
import random

import pyxel


BLACK = 0
WHITE = 7
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 128
PADDLE_WIDTH = 2
PADDLE_HEIGHT = PADDLE_WIDTH * 7
PADDLE_SPEED = 1
BALL_SIZE = 1
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
        self.hitbox = set()

    def calculate_hitbox(self):
        self.hitbox.clear()
        for x in range(self.x - 1, self.x + PADDLE_WIDTH + 1):
            for y in range(self.y - 1, self.y + PADDLE_HEIGHT + 1):
                self.hitbox.add((x, y))


class Pong:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Pong", fps=60, quit_key=pyxel.KEY_ESCAPE)
        self.ball = Ball(*BALL_PARAMS)
        self.player_left = Paddle(SCREEN_WIDTH - SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        self.player_right = Paddle(SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT // 2)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.ball.update()
        self.player_right.calculate_hitbox()
        self.player_left.calculate_hitbox()

        # Paddles Movement
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            if self.player_left.y > SCREEN_HEIGHT - SCREEN_HEIGHT:
                self.player_left.y -= PADDLE_SPEED
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            if self.player_left.y < SCREEN_HEIGHT - PADDLE_HEIGHT:
                self.player_left.y += PADDLE_SPEED
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_2_UP):
            if self.player_right.y > SCREEN_HEIGHT - SCREEN_HEIGHT:
                self.player_right.y -= PADDLE_SPEED
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_2_DOWN):
            if self.player_right.y < SCREEN_HEIGHT - PADDLE_HEIGHT:
                self.player_right.y += PADDLE_SPEED

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
        pyxel.cls(BLACK)

        # Ball
        pyxel.circ(
            self.ball.pos.x,
            self.ball.pos.y,
            BALL_SIZE,
            WHITE
        )

        # Paddles
        pyxel.rect(
            self.player_left.x,
            self.player_left.y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            WHITE
        )
        pyxel.rect(
            self.player_right.x,
            self.player_right.y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            WHITE
        )

        # Middle Line
        pyxel.line(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - SCREEN_HEIGHT,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT,
            WHITE
        )

        # Left Score
        pyxel.text(
            SCREEN_WIDTH // 2 - 7,
            SCREEN_HEIGHT - SCREEN_HEIGHT,
            str(self.player_left.score),
            WHITE
        )

        # Right Score
        pyxel.text(
            SCREEN_WIDTH // 2 + 5,
            SCREEN_HEIGHT - SCREEN_HEIGHT,
            str(self.player_right.score),
            WHITE
        )


if __name__ == '__main__':
    Pong()
