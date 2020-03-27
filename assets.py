"""Assets for game
"""
import pygame

screen_width = 800
screen_height = 600
FPS = 60

player_speed = 0 #TODO: change redundant variable name into class methods
player_control_speed = 6
opponent_speed = 7
ball_speed_x = 7
ball_speed_y = 7

# Game Rectangles
ball = pygame.Rect(int(screen_width / 2 - 15), int(screen_height / 2 - 15), 30, 30) # set initial position of ball
player = pygame.Rect(int(screen_width - 20), int(screen_height / 2 - 70), 10,140) # set initial position of player1, rhs
opponent = pygame.Rect(10, int(screen_height / 2 - 70), 10,140) # set initial position of player2

class color:
	light_grey = (200,200,200)  # color for assets
	bg_color = (0, 0, 0)        # black background
	white=(255, 255, 255)
	yellow=(255, 255, 0)
	black=(0, 0, 0)

def setup():
	"""Setup the screen and clock"""
	global screen, clock
	pygame.init() 
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((screen_width,screen_height)) # screen display 
	pygame.display.set_caption('Pong')  #caption

	
def draw_playing_field():
    """Draw the field of the game"""
    screen.fill(color.bg_color) # fill background color
    pygame.draw.rect(screen, color.light_grey, player) # draw player 1 
    pygame.draw.rect(screen, color.light_grey, opponent) # draw player 2
    pygame.draw.rect(screen, color.light_grey, ball)  # draw ball 
    pygame.draw.aaline(screen, color.light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height)) # draw middle line
    pygame.display.flip() #for updating content of the entire display

def update_FPS():
    pygame.display.flip()
    clock.tick(FPS)

if __name__ == '__main__':
    setup()
    draw_playing_field()