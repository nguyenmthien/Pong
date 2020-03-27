import pygame
import assets
from assets import color

assets.setup()

global title,font,font2,selected,num
num = 0
selected="SINGLE PLAYER"
font2 = pygame.font.SysFont(None,20)
title = pygame.image.load("title.jpg")
font = pygame.font.Font("Pokemon.ttf", 20)

# text render
def text_render(text_name, font, color, surface, x, y):
    textobj = font.render(text_name,1,color) #render the object
    textrect = textobj.get_rect()
    textrect.center = (x,y)   # centric text
    surface.blit(textobj, textrect)  # draw textobj to the screen 

def main_menu():
    global num, selected
    assets.screen.fill(assets.color.black) # black screen
    assets.screen.blit(title ,(178,0))
        
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
        choice_1 = text_render("SINGLE PLAYER", font, assets.color.yellow, assets.screen, 400, 350)
    else:
        choice_1 = text_render("SINGLE PLAYER", font, assets.color.white, assets.screen, 400, 350)
    if selected == "MULTI LOCAL PLAYER":
        choice_2 = text_render("MULTI LOCAL PLAYER", font, assets.color.yellow, assets.screen, 400, 420)
    else:
        choice_2 = text_render("MULTI LOCAL PLAYER", font, assets.color.white, assets.screen, 400, 420)
    if selected == "QUIT":
        choice_3 = text_render("QUIT", font, assets.color.yellow, assets.screen, 400, 490)
    else:
        choice_3 = text_render("QUIT", font, assets.color.white, assets.screen, 400, 490)
    text_render("by Pham Kim Lan, Nguyen Minh Thien, EEIT2017" , font2, color.white, assets.screen, 158, 593)
    
    assets.update_FPS() # update screen
    
if __name__ == '__main__':
    while True:
        main_menu()
