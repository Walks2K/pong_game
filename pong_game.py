"""
Pong game in PyGame
"""


import pygame
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


class Ball:
    """
    Ball class
    """

    def __init__(self, x, y, radius, screen, colour=WHITE):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen
        self.colour = colour

        self.dx = random.choice([-6, 6])
        self.dy = random.choice([-6, 6])

    def move(self):
        """
        Move ball
        """
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        """
        Draw ball
        """
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

    def bounce(self, paddles):
        """
        Bounce ball off top/bottom or paddles
        """
        if self.y <= self.radius:
            self.dy = -self.dy
        elif self.y >= self.screen.get_height() - self.radius:
            self.dy = -self.dy

        for paddle in paddles:
            if self.x >= paddle.x - self.radius and self.x <= paddle.x + paddle.width + self.radius:
                if self.y >= paddle.y - self.radius and self.y <= paddle.y + paddle.height + self.radius:
                    self.dx = -self.dx

    def reset(self):
        """
        Reset ball
        """
        self.x = self.screen.get_width() / 2
        self.y = self.screen.get_height() / 2
        self.dx = random.choice([-6, 6])
        self.dy = random.choice([-6, 6])


class Paddle:
    """
    Paddle class
    """

    def __init__(self, x, y, width, height, screen, colour=WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.colour = colour

        self.movement_speed = 5
        self.dy = 0
        self.score = 0

    def move(self):
        """
        Move paddle - ensuring it stays within bounds
        """
        self.y += self.dy

        if self.y <= 0:
            self.y = 0
        elif self.y + self.height >= self.screen.get_height():
            self.y = self.screen.get_height() - self.height

    def draw(self, screen):
        """
        Draw paddle
        """
        pygame.draw.rect(screen, self.colour,
                         (self.x, self.y, self.width, self.height))


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
            if event.key == pygame.K_UP:
                self.move_up()
            elif event.key == pygame.K_DOWN:
                self.move_down()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.stop_moving()

    def move_up(self):
        """
        Move paddle up
        """
        self.paddle.dy = -self.paddle.movement_speed

    def move_down(self):
        """
        Move paddle down
        """
        self.paddle.dy = self.paddle.movement_speed

    def stop_moving(self):
        """
        Stop paddle movement
        """
        self.paddle.dy = 0


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
        if self.ball.y > self.paddle.y + self.paddle.height / 2:
            self.paddle.dy = self.paddle.movement_speed
        elif self.ball.y < self.paddle.y + self.paddle.height / 2:
            self.paddle.dy = -self.paddle.movement_speed
        else:
            self.paddle.dy = 0


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

        self.ball = Ball(self.width / 2, self.height / 2, 10, self.screen)
        self.paddles = [Paddle(10, self.height / 2 - 50, 10, 100, self.screen),
                        Paddle(self.width - 20, self.height / 2 - 50, 10, 100, self.screen)]
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
        if self.ball.x <= 0:
            self.ball.reset()
            self.ai.score += 1
        elif self.ball.x >= self.width:
            self.ball.reset()
            self.player.score += 1

    def update(self):
        """
        Update game
        """
        self.ball.move()
        self.ball.bounce(self.paddles)
        self.check_boundaries()

        self.player.paddle.move()
        self.ai.paddle.move()

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
