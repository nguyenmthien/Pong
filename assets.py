"""Assets for game
"""
import random
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
pygame.font.init()
DISPLAY_FONT = pygame.font.Font('font.ttf', 80)

COLOR = {
    'light_grey': (200, 200, 200),
    'white'     : (255, 255, 255),
    'yellow'    : (255, 255, 0),
    'black'     : (0, 0, 0),
}


class Assets:
    """Default assets class"""
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # screen display
        pygame.display.set_caption('Pong')  #caption
        self.player = Paddle('right')
        self.opponent = Paddle('left')
        self.ball = Ball()

    def draw_playing_field(self):
        """Draw the field of the game"""
        self.screen.fill(COLOR["black"]) # fill background color
        pygame.draw.rect(self.screen, COLOR["light_grey"], self.player.rect) # draw player 1
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.opponent.rect) # draw player 2
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.ball.rect)  # draw ball
        pygame.draw.aaline(self.screen,
                           COLOR['light_grey'],
                           (SCREEN_WIDTH / 2, 0),
                           (SCREEN_WIDTH / 2, SCREEN_HEIGHT)) # draw middle line
        self.screen.blit(self.player.score, (int(3/4*SCREEN_WIDTH - 20), 20))
        self.screen.blit(self.opponent.score, (int(SCREEN_WIDTH/4 - 20), 20))
        self.maintain_fps()

    def draw_client(self):
        """Draw the field in client mode"""
        self.screen.fill(COLOR['black']) # fill background color
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.player.rect) # draw player 1
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.opponent.rect) # draw player 2
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.ball.rect)  # draw ball
        pygame.draw.aaline(self.screen,
                           COLOR['light_grey'],
                           (SCREEN_WIDTH / 2, 0),
                           (SCREEN_WIDTH / 2, SCREEN_HEIGHT)) # draw middle line
        self.screen.blit(self.player.score, (int(3/4*SCREEN_WIDTH - 20), 20))
        self.screen.blit(self.opponent.score, (int(SCREEN_WIDTH/4 - 20), 20))


    def maintain_fps(self):
        """Make sure game run at assests.FPS"""
        pygame.display.flip()
        self.clock.tick(FPS)


class Paddle:
    """Class for manipulating the paddles"""
    def __init__(self, location='right'):
        if location is 'right':
            self.rect = pygame.Rect(int(SCREEN_WIDTH - 20),
                                    int(SCREEN_HEIGHT / 2 - 70),
                                    10,
                                    140)
        if location is 'left':
            self.rect = pygame.Rect(10,
                                    int(SCREEN_HEIGHT / 2 - 70),
                                    10,
                                    140)
        self.speed = 0
        self.previous_speed = 0
        self.ai_speed = 7
        self.control_speed = 6
        self.score_value = 0
        self.score = DISPLAY_FONT.render(str(self.score_value), 1, COLOR["light_grey"])

    def animation(self):
        """Animation of player"""
        self.rect.y += self.speed

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def increase_score(self):
        """Increase and draw score of player"""
        self.score_value += 1
        self.score = DISPLAY_FONT.render(str(self.score_value),
                                         1,
                                         COLOR['light_grey'])

    def reset(self):
        """Reset score and position"""
        self.score_value = 0
        self.rect.centery = int(SCREEN_HEIGHT/2)

    def artificial_intelligence(self, ball_y: int):
        """Single-player AI"""
        if self.rect.top < ball_y:
            self.rect.y += self.ai_speed
        if self.rect.bottom > ball_y:
            self.rect.y -= self.ai_speed

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Ball:
    """Class for manipulating the ball"""
    def __init__(self):
        self.rect = pygame.Rect(int(SCREEN_WIDTH / 2 - 15),
                                int(SCREEN_HEIGHT / 2 - 15),
                                30,
                                30) # set initial position of ball
        self.speed_x = 7
        self.speed_y = 7
        self.speed_y_initial = 7
        self.speed_y_modifier = 1/4

    def animation(self, opponent: Paddle, player: Paddle):
        """Animation and logic of ball"""
        self.change_position()
        self.check_collision_wall(opponent, player)
        self.check_collision_paddle(opponent, player)

    def start(self):
        """Replace the ball to the origin"""
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.speed_y = self.speed_y_initial*random.choice((1, -1))
        self.speed_x *= random.choice((1, -1))

    def change_position(self):
        """Update position of ball"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def check_collision_wall(self, opponent: Paddle, player: Paddle):
        """Check colision and change movement of ball with wall"""
        if  self.rect.right >= SCREEN_WIDTH:
            self.start()
            opponent.increase_score()

        if self.rect.left <= 0:
            self.start()
            player.increase_score()

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

    def check_collision_paddle(self, opponent: Paddle, player: Paddle):
        """Check colision and change movement of ball with paddles"""
        if self.rect.colliderect(opponent.rect):
            self.speed_x *= -1
            self.speed_y = int((self.rect.centery - opponent.rect.centery)
                               * self.speed_y_modifier)

        if self.rect.colliderect(player.rect):
            self.speed_x *= -1
            self.speed_y = int((self.rect.centery - player.rect.centery)
                               * self.speed_y_modifier)


if __name__ == '__main__':
    # setup()
    # draw_playing_field()
    pass
