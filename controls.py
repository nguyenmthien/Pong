"""Input for game
"""
import sys
import pygame
import assets
import ui
import animation


class Control:
    """All controls for game"""
    def __init__(self):
        self.current_menu = "title screen"

    def game_input(self):
        """Singleplayer input handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    assets.player_speed -= assets.player_control_speed
                if event.key == pygame.K_DOWN:
                    assets.player_speed += assets.player_control_speed
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end single player")
                    animation.reset()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    assets.player_speed += assets.player_control_speed
                if event.key == pygame.K_DOWN:
                    assets.player_speed -= assets.player_control_speed

    def title_screen(self):
        """Title screen input handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if ui.choice > 0:
                        ui.choice -= 1
                elif event.key == pygame.K_DOWN:
                    if ui.choice < 3:
                        ui.choice += 1
                if event.key == pygame.K_RETURN:
                    if ui.selection_list[ui.choice] == "SINGLE PLAYER":
                        print("start single player")
                        self.current_menu = "single player"
                    if ui.selection_list[ui.choice] == "LOCAL MULTIPLAYER":
                        print("start single player")
                        self.current_menu = "local multiplayer"
                    if ui.selection_list[ui.choice] == "QUIT":
                        pygame.quit()
                        sys.exit()

    def local_multiplayer(self):
        """Local multiplayer inputs handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    assets.player_speed -= assets.player_control_speed
                if event.key == pygame.K_DOWN:
                    assets.player_speed += assets.player_control_speed
                if event.key == pygame.K_w:
                    assets.opponent_speed -= assets.opponent_control_speed
                if event.key == pygame.K_s:
                    assets.opponent_speed += assets.opponent_control_speed
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end local multiplayer")
                    animation.reset()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    assets.player_speed += assets.player_control_speed
                if event.key == pygame.K_DOWN:
                    assets.player_speed -= assets.player_control_speed
                if event.key == pygame.K_w:
                    assets.opponent_speed += assets.opponent_control_speed
                if event.key == pygame.K_s:
                    assets.opponent_speed -= assets.opponent_control_speed
    def client(self):
        """Client mode input handler"""
        assets.opponent_previous_speed = assets.opponent_speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    assets.opponent_speed -= assets.opponent_control_speed
                if event.key == pygame.K_s:
                    assets.opponent_speed += assets.opponent_control_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    assets.opponent_speed += assets.opponent_control_speed
                if event.key == pygame.K_s:
                    assets.opponent_speed -= assets.opponent_control_speed
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end local multiplayer")
                    animation.reset()

            if assets.opponent_speed == assets.opponent_previous_speed:
                pass
