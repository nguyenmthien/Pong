"""Assets for game
"""
import pygame
import os

class Color:
    light_grey = (200,200,200)  # color for assets
    white=(255, 255, 255)
    yellow=(255, 255, 0)
    black=(0, 0, 0)
pygame.font.init()
display_font = pygame.font.Font('font.ttf', 80)

screen_width = 800
screen_height = 600
FPS = 60

player = pygame.Rect(int(screen_width - 20), int(screen_height / 2 - 70), 10,140) # set initial position of player1, rhs
player_speed = 0 #TODO: change redundant variable name into class methods
player_control_speed = 6
player_score_value = 0
player_score = display_font.render(str(player_score_value), 1, Color.light_grey)

opponent = pygame.Rect(10, int(screen_height / 2 - 70), 10,140) # set initial position of player2
opponent_ai_speed = 7
opponent_speed = 0
opponent_control_speed = 6
opponent_score_value = 0
opponent_score = display_font.render(str(opponent_score_value), 1, Color.light_grey)

ball = pygame.Rect(int(screen_width / 2 - 15), int(screen_height / 2 - 15), 30, 30) # set initial position of ball
ball_speed_x = 7
ball_speed_y = 7
ball_speed_y_initial = 7
ball_speed_y_modifier = 1/4



def setup():
    """Setup the screen and clock"""
    global screen, clock
    pygame.init() 
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width,screen_height)) # screen display 
    pygame.display.set_caption('Pong')  #caption

    
def draw_playing_field():
    """Draw the field of the game"""
    screen.fill(Color.black) # fill background color
    pygame.draw.rect(screen, Color.light_grey, player) # draw player 1 
    pygame.draw.rect(screen, Color.light_grey, opponent) # draw player 2
    pygame.draw.rect(screen, Color.light_grey, ball)  # draw ball 
    pygame.draw.aaline(screen, Color.light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height)) # draw middle line
    screen.blit(player_score, (int(3/4*screen_width - 20), 20))
    screen.blit(opponent_score, (int(screen_width/4 - 20), 20))
    update_FPS()

def update_FPS():
    pygame.display.flip()
    clock.tick(FPS)

if __name__ == '__main__':
    setup()
    draw_playing_field()