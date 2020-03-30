"""Various functions for the user interface
"""
import pygame
import assets

pygame.font.init()
UI_FONT2 = pygame.font.SysFont(None, 20)
UI_FONT = pygame.font.Font("Pokemon.ttf", 20)

class UserInterface:
    """Default ui class"""
    def __init__(self):
        self.choice = 0
        self.selection_list = ["SINGLE PLAYER",
                               "LOCAL MULTIPLAYER",
                               "HOST GAME",
                               "JOIN GAME",
                               "QUIT"]
        self.selection_xy = [(400, 350),
                             (400, 400),
                             (400, 450),
                             (400, 500),
                             (400, 550)]

    def text_render(self, text_name, font_name, color, surface, coordinate):
        """Render text_name to surface"""
        textobj = font_name.render(text_name, 1, color) #render the object
        textrect = textobj.get_rect()
        textrect.center = coordinate   # centric text
        surface.blit(textobj, textrect)  # draw textobj to the screen

    def title_screen(self, asset_class: assets.Assets):
        """Draw the title screen"""
        title = pygame.image.load("title.jpg")
        asset_class.screen.fill(assets.COLOR['black']) # black screen
        asset_class.screen.blit(title, (178, 0))

        for i, text in enumerate(self.selection_list):
            if text == self.selection_list[self.choice]:
                self.text_render(text,
                                 UI_FONT,
                                 assets.COLOR['yellow'],
                                 asset_class.screen,
                                 self.selection_xy[i])
            else:
                self.text_render(text,
                                 UI_FONT,
                                 assets.COLOR['white'],
                                 asset_class.screen,
                                 self.selection_xy[i])

        self.text_render("by Pham K. Lan, Nguyen M. Thien, EEIT2017",
                         UI_FONT2,
                         assets.COLOR['white'],
                         asset_class.screen,
                         (158, 593))

        asset_class.maintain_fps() # update screen


if __name__ == '__main__':
    ASSET = assets.Assets()
    USER_INTERFACE = UserInterface()
    USER_INTERFACE.title_screen(ASSET)
