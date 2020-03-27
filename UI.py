import pygame
import assets
from pygame.locals import *

light_grey = (200,200,200)  # color for assets
bg_color = (0, 0, 0)        # black background
white=(255, 255, 255)
yellow=(255, 255, 0)
black=(0, 0, 0)
FPS = 60

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Pong')
screen = pygame.display.set_mode((800,600))
font2 = pygame.font.SysFont(None,20)
pong_title = pygame.image.load("pong-title.jpg")
font = pygame.font.Font("PokemonGb-RAeo.ttf", 20)

options = ['Single player', 'Multiplayer', 'Quit']

# text render
def text_render(text_name, font, color, surface, x, y):
    textobj = font.render(text_name,1,color) #render the object
    textrect = textobj.get_rect()
    textrect.center = (x,y)   # centric text
    surface.blit(textobj, textrect)  # draw textobj to the screen 

def main_menu():
    selected="SINGLE PLAYER"
    num = 0 
    
    while True:
        screen.fill(black) # black screen
        screen.blit(pong_title,(178,0)) 
        
        # input logic
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    num += 1
                elif event.key==pygame.K_DOWN:
                    num -= 1
                if event.key==pygame.K_RETURN:
                    if selected == "SINGLE PLAYER":
                        print("start")
                    if selected == "QUIT":
                        pygame.quit()
                        quit()
                        
        # text selection			
        if num == 0:
            selected = "SINGLE PLAYER"
        elif num == -1:
            selected = "MULTI LOCAL PLAYER"
        elif num == -2:
            selected = "QUIT"
            
        # text output
        if selected == "SINGLE PLAYER":
            choice_1 = text_render("SINGLE PLAYER", font, yellow, screen, 400, 350)
        else:
            choice_1 = text_render("SINGLE PLAYER", font, white, screen, 400, 350)
        if selected == "MULTI LOCAL PLAYER":
            choice_2 = text_render("MULTI LOCAL PLAYER", font, yellow, screen, 400, 420)
        else:
            choice_2 = text_render("MULTI LOCAL PLAYER", font, white, screen, 400, 420)
        if selected == "QUIT":
            choice_3 = text_render("QUIT", font, yellow, screen, 400, 490)
        else:
            choice_3 = text_render("QUIT", font, white, screen, 400, 490)
        text_render("by Pham Kim Lan, Nguyen Minh Thien, EEIT2017" , font2, white, screen, 158, 593)
        
        pygame.display.update()
        clock.tick(FPS)

main_menu()

