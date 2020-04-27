"""Assets for game
"""
import math
import random
import pygame

#These are global assets constants. The names should self-explainatory
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
pygame.font.init()
DISPLAY_FONT = pygame.font.Font('font.ttf', 80)
UI_FONT2 = pygame.font.Font("font.ttf", 15)
UI_FONT = pygame.font.Font("font.ttf", 30)

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
        pygame.draw.rect(self.screen, COLOR["light_grey"], self.player.rect)  # draw player 1
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.opponent.rect)  # draw player 2
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.ball.rect)  # draw ball
        draw_dashed_line(self.screen,
                         COLOR['light_grey'],
                         (SCREEN_WIDTH / 2, 0),
                         (SCREEN_WIDTH / 2, SCREEN_HEIGHT),
                         9,
                         30)  # draw middle line
        self.screen.blit(self.player.score, (int(1/2*SCREEN_WIDTH+20), 20))
        self.screen.blit(self.opponent.score, (int(1/2*SCREEN_WIDTH-90), 20))

    def draw_indicators_ai(self):
        """Add player indicators in single player mode"""
        self.screen.blit(self.player.indicator_p1, (int(1/2*SCREEN_WIDTH+20), 520))
        self.screen.blit(self.player.indicator_com, (int(1/2*SCREEN_WIDTH-90), 520))
        self.maintain_fps()

    def draw_indicators(self):
        """Add player indicators in multiplayer mode"""
        self.screen.blit(self.player.indicator_p1, (int(1/2*SCREEN_WIDTH+20), 520))
        self.screen.blit(self.player.indicator_p2, (int(1/2*SCREEN_WIDTH-90), 520))
        self.maintain_fps()

    def draw_client(self):
        """Draw the field in client mode"""
        self.screen.fill(COLOR['black']) # fill background color
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.player.rect) # draw player 1
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.opponent.rect) # draw player 2
        pygame.draw.rect(self.screen, COLOR['light_grey'], self.ball.rect)  # draw ball
        draw_dashed_line(self.screen,
                         COLOR['light_grey'],
                         (SCREEN_WIDTH / 2, 0),
                         (SCREEN_WIDTH / 2, SCREEN_HEIGHT),
                         9,
                         30) # draw middle line
        self.player.score = DISPLAY_FONT.render(str(self.player.score_value),
                                                1,
                                                COLOR['light_grey'])
        self.opponent.score = DISPLAY_FONT.render(str(self.opponent.score_value),
                                                  1,
                                                  COLOR['light_grey'])
        self.screen.blit(self.player.score, (int(1/2*SCREEN_WIDTH+60), 20))
        self.screen.blit(self.opponent.score, (int(1/2*SCREEN_WIDTH-90), 20))
        pygame.display.flip()

    def maintain_fps(self):
        """Make sure game run at assests.FPS"""
        pygame.display.flip()
        self.clock.tick(FPS)

    def get_coordinates(self):
        """Return assets center coordinates"""
        return {'ball'             :self.ball.rect.center,
                'player'           :self.player.rect.center,
                'opponent'         :self.opponent.rect.center,
                'player score'     :self.player.score_value,
                'opponent score'   :self.opponent.score_value}

    def set_coordinates(self, coords: dict):
        """Assign coordinates to the object"""
        self.ball.rect.center = coords['ball']
        self.player.rect.center = coords['player']
        self.opponent.rect.center = coords['opponent']
        self.player.score_value = coords['player score']
        self.opponent.score_value = coords['opponent score']

    def get_opponent_speed(self):
        """Return opponent speed"""
        return self.opponent.speed

    def set_opponent_speed(self, speed: int):
        """set opponent speed"""
        self.opponent.speed = speed

    def reset(self):
        """Reset the ball's and paddle's position & scores"""
        self.player.reset()
        self.opponent.reset()
        self.ball.start()


class Paddle:
    """Class for manipulating the paddles"""
    def __init__(self, location='right'):
        if location == 'right':
            self.rect = pygame.Rect(int(SCREEN_WIDTH - 20),
                                    int(SCREEN_HEIGHT / 2 - 70),
                                    10,
                                    140)
        if location == 'left':
            self.rect = pygame.Rect(10,
                                    int(SCREEN_HEIGHT / 2 - 70),
                                    10,
                                    140)
        self.speed = 0
        self.previous_speed = 0
        self.ai_speed = 7
        self.control_speed = 6
        self.score_value = 0
        self.score = DISPLAY_FONT.render(str(self.score_value),
                                         1,
                                         COLOR["light_grey"])
        self.indicator_p1 = DISPLAY_FONT.render("P1",
                                                1,
                                                COLOR['light_grey'])
        self.indicator_com = DISPLAY_FONT.render("ai",
                                                 1,
                                                 COLOR['light_grey'])
        self.indicator_p2 = DISPLAY_FONT.render("P2",
                                                1,
                                                COLOR['light_grey'])

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
        self.score = DISPLAY_FONT.render(str(self.score_value),
                                         1,
                                         COLOR['light_grey'])
        self.speed = 0

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


class UserInterface:
    """Default UI class"""
    def __init__(self):
        self.choice = 0
        self.selection_list = ["SINGLE PLAYER",
                               "LOCAL MULTIPLAYER",
                               "HOST GAME",
                               "JOIN GAME",
                               "QUIT"]
        self.selection_xy = [(400, 325),
                             (400, 375),
                             (400, 425),
                             (400, 475),
                             (400, 525)]
        self.current_menu = "TITLE SCREEN"

    def title_screen(self, asset_obj: Assets):
        """Draw the title screen"""
        title = pygame.image.load("title.jpg")
        asset_obj.screen.fill(COLOR['black'])
        asset_obj.screen.blit(title, (178, 0))

        for i, text in enumerate(self.selection_list):
            if text == self.selection_list[self.choice]:
                text_render(text,
                            UI_FONT,
                            COLOR['yellow'],
                            asset_obj.screen,
                            self.selection_xy[i])
            else:
                text_render(text,
                            UI_FONT,
                            COLOR['white'],
                            asset_obj.screen,
                            self.selection_xy[i])

        text_render("by Nguyen M. Thien, Pham K. Lan, Nguyen K. Thinh, EEIT2017",
                    UI_FONT2,
                    COLOR['white'],
                    asset_obj.screen,
                    (400, 593))

        asset_obj.maintain_fps() # update screen

    def wait_for_client(self, asset_obj: Assets, ip_addr: str):
        """Use when waiting for client in server mode"""
        asset_obj.screen.fill(COLOR['black'])
        text_render("WAITING FOR CLIENT",
                    UI_FONT,
                    COLOR['white'],
                    asset_obj.screen,
                    (400, 250))
        text_render(f"YOUR IP ADDRESS IS {ip_addr}",
                    UI_FONT,
                    COLOR['white'],
                    asset_obj.screen,
                    (400, 300))
        text_render("PRESS ESC TO EXIT TO TITLE SCREEN",
                    UI_FONT,
                    COLOR['white'],
                    asset_obj.screen,
                    (400, 350))
        asset_obj.maintain_fps()

    def choose_server(self, asset_obj: Assets, server_ip_list: list):
        """Server choosing screen, use in client mode"""
        asset_obj.screen.fill(COLOR['black'])

        text_render("CHOOSE YOUR DESIRED SERVER",
                    UI_FONT,
                    COLOR['white'],
                    asset_obj.screen,
                    (400, 125))
        text_render("PRESS ESC TO EXIT TO TITLE SCREEN",
                    UI_FONT,
                    COLOR['white'],
                    asset_obj.screen,
                    (400, 175))
        text_render("PRESS F5 TO REFRESH SERVER LIST",
                    UI_FONT,
                    COLOR['white'],
                    asset_obj.screen,
                    (400, 225))

        for i, text in enumerate(server_ip_list):
            if text == server_ip_list[self.choice]:
                text_render(text,
                            UI_FONT,
                            COLOR['yellow'],
                            asset_obj.screen,
                            self.selection_xy[i])
            else:
                text_render(text,
                            UI_FONT,
                            COLOR['white'],
                            asset_obj.screen,
                            self.selection_xy[i])

        asset_obj.maintain_fps()

    def wait_for_search(self, asset_obj: Assets):
        """Use in client mode while seraching for server"""
        asset_obj.screen.fill(COLOR['black'])

        text_render("SEARCHING FOR LOCAL SERVERS...",
                    UI_FONT,
                    COLOR['white'],
                    asset_obj.screen,
                    (400, 300))
        asset_obj.maintain_fps()


def text_render(text_name, font_name, color, surface, coordinate):
    """Render text_name to surface"""
    textobj = font_name.render(text_name, 1, color) #render the object
    textrect = textobj.get_rect()
    textrect.center = coordinate   # centric text
    surface.blit(textobj, textrect)  # draw textobj to the screen


class Point:
    """Manipulating coordinates"""
    # constructed using a normal tupple
    def __init__(self, point_t=(0, 0)):
        self.x_coord = float(point_t[0])
        self.y_coord = float(point_t[1])
    # define all useful operators
    def __add__(self, other):
        return Point((self.x_coord + other.x_coord, self.y_coord + other.y_coord))
    def __sub__(self, other):
        return Point((self.x_coord - other.x_coord, self.y_coord - other.y_coord))
    def __mul__(self, scalar):
        return Point((self.x_coord*scalar, self.y_coord*scalar))
    def __truediv__(self, scalar):
        return Point((self.x_coord/scalar, self.y_coord/scalar))
    def __len__(self):
        return int(math.sqrt(self.x_coord**2 + self.y_coord**2))
    # get back values in original tuple format
    def get(self):
        """Default class getter"""
        return (self.x_coord, self.y_coord)

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    """Draw dashed line with arguments"""
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement/length

    for index in range(0, int(length/dash_length), 2):
        start = origin + (slope *    index    * dash_length)
        end = origin + (slope * (index + 1) * dash_length)
        pygame.draw.line(surf, color, start.get(), end.get(), width)


if __name__ == '__main__':
    ASSETS = Assets()
    UI = UserInterface()
    UI.wait_for_client(ASSETS, "192.168.0.12")
    import time
    time.sleep(3)
    UI.wait_for_search(ASSETS)
    time.sleep(3)
