import pygame
import assets
from assets import color


# text render
def text_render(text_name, font, color, surface, xy):
    textobj = font.render(text_name,1,color) #render the object
    textrect = textobj.get_rect()
    textrect.center = xy   # centric text
    surface.blit(textobj, textrect)  # draw textobj to the screen 

def initialize_menu():
    global font, font2, menu
    pygame.font.init()
    font2 = pygame.font.SysFont(None,20)
    font = pygame.font.Font("Pokemon.ttf", 20)

def initialize_title_screen():
    global title, choice, selection_list, selection_xy
    choice = 0
    selection_list = ["SINGLE PLAYER", "LOCAL MULTIPLAYER", "LOCAL NETWORK MULTIPLAYER", "QUIT"]
    selection_xy = [(400, 350), (400, 420), (400, 490), (400, 550)]
    title = pygame.image.load("title.jpg")

def main_menu():    
    assets.screen.fill(assets.color.black) # black screen
    assets.screen.blit(title ,(178,0))

    for i in range(len(selection_list)):
        if selection_list[i] == selection_list[choice]:
            text_render(selection_list[i], font, assets.color.yellow, assets.screen, selection_xy[i])
        else:
            text_render(selection_list[i], font, assets.color.white, assets.screen, selection_xy[i])

    text_render("by Pham Kim Lan, Nguyen Minh Thien, EEIT2017" , font2, color.white, assets.screen, (158, 593))
    
    assets.update_FPS() # update screen
    
if __name__ == '__main__':
    initialize_menu()
    initialize_title_screen()
    assets.setup()
    while True:
        main_menu()
