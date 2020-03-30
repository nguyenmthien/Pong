"""Various functions for the user interface
"""
import pygame
import assets

pygame.font.init()
font2 = pygame.font.SysFont(None, 20)
font = pygame.font.Font("Pokemon.ttf", 20)

def text_render(text_name, font_name, color, surface, coordinate):
    """Render text_name to surface"""
    textobj = font_name.render(text_name, 1, color) #render the object
    textrect = textobj.get_rect()
    textrect.center = coordinate   # centric text
    surface.blit(textobj, textrect)  # draw textobj to the screen


def initialize_title_screen():
    """Initialize title screen variables"""
    global choice, selection_list, selection_xy
    choice = 0
    selection_list = ["SINGLE PLAYER", "LOCAL MULTIPLAYER", "LOCAL NETWORK MULTIPLAYER", "QUIT"]
    selection_xy = [(400, 350), (400, 420), (400, 490), (400, 550)]


def main_menu():
    """Draw the title screen"""
    title = pygame.image.load("title.jpg")
    assets.screen.fill(assets.Color.black) # black screen
    assets.screen.blit(title, (178, 0))

    for i in range(len(selection_list)):
        if selection_list[i] == selection_list[choice]:
            text_render(selection_list[i],
                        font,
                        assets.Color.yellow,
                        assets.screen,
                        selection_xy[i])
        else:
            text_render(selection_list[i],
                        font,
                        assets.Color.white,
                        assets.screen,
                        selection_xy[i])

    text_render("by Pham K. Lan, Nguyen M. Thien, EEIT2017",
                font2,
                assets.Color.white,
                assets.screen,
                (158, 593))

    assets.update_FPS() # update screen


if __name__ == '__main__':
    initialize_title_screen()
    assets.setup()
    while True:
        main_menu()
