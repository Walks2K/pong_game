"""
Pong game in PyGame
"""


import pygame
import pygame.gfxdraw
import random


# Define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Game parameters
WIDTH = 800
HEIGHT = 600
TITLE = "Pong Game"
FPS = 60


pygame.font.init()


class Ball(pygame.sprite.Sprite):
    """
    Ball class
    """

    def __init__(self, radius=10, colour=WHITE, movement_speed=6):
        super().__init__()

        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        self.movement_speed = movement_speed
        self.x_vel = random.choice([-self.movement_speed, self.movement_speed])
        self.y_vel = random.choice([-self.movement_speed, self.movement_speed])

    def update(self, paddles=None):
        """
        Process ball movement - bouncing off paddles and walls
        """
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.y_vel *= -1
            self.rect.y += self.y_vel

        if paddles is not None:
            for paddle in paddles:
                if self.rect.colliderect(paddle.rect):
                    self.x_vel *= -1
                    self.rect.x += self.x_vel
                    self.y_vel *= -1
                    self.rect.y += self.y_vel

    def draw(self, screen):
        """
        Draw ball
        """
        pygame.gfxdraw.aacircle(screen, self.rect.centerx,
                                self.rect.centery, self.rect.width // 2, WHITE)
        pygame.gfxdraw.filled_circle(
            screen, self.rect.centerx, self.rect.centery, self.rect.width // 2, WHITE)

    def reset(self):
        """
        Reset ball
        """
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.x_vel = random.choice([-self.movement_speed, self.movement_speed])
        self.y_vel = random.choice([-self.movement_speed, self.movement_speed])


class Paddle(pygame.sprite.Sprite):
    """
    Paddle class
    """

    def __init__(self, x, y, width=10, height=100, colour=WHITE, movement_speed=5):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.movement_speed = movement_speed
        self.y_vel = 0

    def update(self):
        """
        Update paddle position - ensuring it stays within the screen
        """
        self.rect.y += self.y_vel

        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def move_up(self):
        """
        Move paddle up
        """
        self.y_vel = -self.movement_speed

    def move_down(self):
        """
        Move paddle down
        """
        self.y_vel = self.movement_speed

    def move_stop(self):
        """
        Stop paddle
        """
        self.y_vel = 0

    def draw(self, screen):
        """
        Draw paddle
        """
        pygame.draw.rect(screen, WHITE, self.rect)

    def reset(self):
        """
        Reset paddle
        """
        self.rect.center = (WIDTH / 2, HEIGHT / 2)


class Player:
    """
    Player class
    """

    def __init__(self, paddle):
        self.paddle = paddle
        self.score = 0

    def handle_event(self, event):
        """
        Handle events
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.paddle.move_up()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.paddle.move_down()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.paddle.move_stop()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.paddle.move_stop()


class SimpleAI:
    """
    Simple AI class
    """

    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball
        self.score = 0

    def move(self):
        """
        Move paddle
        """
        if self.ball.rect.centery < self.paddle.rect.centery:
            self.paddle.move_up()
        elif self.ball.rect.centery > self.paddle.rect.centery:
            self.paddle.move_down()
        else:
            self.paddle.move_stop()


class Game:
    """
    Game class
    """

    def __init__(self, width, height, title, fps):
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.ball = Ball()
        self.paddles = [Paddle(20, HEIGHT / 2 - 100),
                        Paddle(WIDTH - 20, HEIGHT / 2 - 100)]
        self.player = Player(self.paddles[0])
        self.ai = SimpleAI(self.paddles[1], self.ball)

        self.running = True

    def run(self):
        """
        Run game
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        """
        Handle events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.player.handle_event(event)

        self.ai.move()

    def check_boundaries(self):
        """
        Check ball boundaries
        """
        if self.ball.rect.x <= 0:
            self.ball.reset()
            self.ai.score += 1
        elif self.ball.rect.x + self.ball.rect.width >= self.width:
            self.ball.reset()
            self.player.score += 1

        if self.ball.rect.y <= 0:
            self.ball.y_vel = abs(self.ball.y_vel)
        elif self.ball.rect.y + self.ball.rect.height >= self.height:
            self.ball.y_vel = -abs(self.ball.y_vel)

    def update(self):
        """
        Update game
        """
        self.ball.update(self.paddles)
        self.check_boundaries()

        for paddle in self.paddles:
            paddle.update()

    def draw(self):
        """
        Draw game
        """
        self.screen.fill(BLACK)

        self.ball.draw(self.screen)
        self.player.paddle.draw(self.screen)
        self.ai.paddle.draw(self.screen)
        self.draw_scores()

        pygame.display.flip()

        self.clock.tick(self.fps)

    def draw_scores(self):
        """
        Draw scores
        """
        font = pygame.font.SysFont('Arial', 24)
        text = font.render('Player: ' + str(self.player.score), True, WHITE)
        self.screen.blit(text, (10, 10))

        text = font.render('AI: ' + str(self.ai.score), True, WHITE)
        self.screen.blit(text, (self.width - text.get_width() - 10, 10))


def main():
    """
    Main function
    """
    game = Game(WIDTH, HEIGHT, TITLE, FPS)
    game.run()


if __name__ == '__main__':
    main()
