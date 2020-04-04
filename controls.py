"""Input for game
"""
import sys
import pygame
import assets
import networking

class Control:
    """All controls for game"""
    def __init__(self):
        self.current_menu = "title screen"

    def game_input(self, asset_class: assets.Assets):
        """Singleplayer input handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    asset_class.player.speed -= asset_class.player.control_speed
                if event.key == pygame.K_DOWN:
                    asset_class.player.speed += asset_class.player.control_speed
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end single player")
                    asset_class.player.reset()
                    asset_class.opponent.reset()
                    asset_class.ball.start()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    asset_class.player.speed += asset_class.player.control_speed
                if event.key == pygame.K_DOWN:
                    asset_class.player.speed -= asset_class.player.control_speed

    def title_screen(self, ui_class: assets.UserInterface):
        """Title screen input handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exit game")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if ui_class.choice > 0:
                        ui_class.choice -= 1
                elif event.key == pygame.K_DOWN:
                    if ui_class.choice < len(ui_class.selection_list):
                        ui_class.choice += 1
                if event.key == pygame.K_RETURN:
                    if ui_class.selection_list[ui_class.choice] == "SINGLE PLAYER":
                        print("start single player")
                        self.current_menu = "single player"
                    if ui_class.selection_list[ui_class.choice] == "LOCAL MULTIPLAYER":
                        print("start local multiplayer")
                        self.current_menu = "local multiplayer"
                    if ui_class.selection_list[ui_class.choice] == "HOST GAME":
                        print("start host game")
                        self.current_menu = "local network server"
                    if ui_class.selection_list[ui_class.choice] == "JOIN GAME":
                        print("start client")
                        self.current_menu = "local network client"
                    if ui_class.selection_list[ui_class.choice] == "QUIT":
                        print("exit game")
                        pygame.quit()
                        sys.exit()

    def local_multiplayer(self, asset_class: assets.Assets):
        """Local multiplayer inputs handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    asset_class.player.speed -= asset_class.player.control_speed
                if event.key == pygame.K_DOWN:
                    asset_class.player.speed += asset_class.player.control_speed
                if event.key == pygame.K_w:
                    asset_class.opponent.speed -= asset_class.opponent.control_speed
                if event.key == pygame.K_s:
                    asset_class.opponent.speed += asset_class.opponent.control_speed
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end local multiplayer")
                    asset_class.player.reset()
                    asset_class.opponent.reset()
                    asset_class.ball.start()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    asset_class.player.speed += asset_class.player.control_speed
                if event.key == pygame.K_DOWN:
                    asset_class.player.speed -= asset_class.player.control_speed
                if event.key == pygame.K_w:
                    asset_class.opponent.speed += asset_class.opponent.control_speed
                if event.key == pygame.K_s:
                    asset_class.opponent.speed -= asset_class.opponent.control_speed

    def client(self, asset_class: assets.Assets, networking_class: networking.Networking):
        """Client mode input handler"""
        asset_class.opponent.previous_speed = asset_class.opponent.speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    asset_class.opponent.speed -= asset_class.opponent.control_speed
                if event.key == pygame.K_s:
                    asset_class.opponent.speed += asset_class.opponent.control_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    asset_class.opponent.speed += asset_class.opponent.control_speed
                if event.key == pygame.K_s:
                    asset_class.opponent.speed -= asset_class.opponent.control_speed
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end tcp client")
                    asset_class.player.reset()
                    asset_class.opponent.reset()
                    asset_class.ball.start()

            if asset_class.opponent.speed != asset_class.opponent.previous_speed:
                networking_class.send_controls(asset_class)
