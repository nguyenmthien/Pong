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

    def game_input(self, assets_obj: assets.Assets):
        """Singleplayer input handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    assets_obj.player.speed -= assets_obj.player.control_speed
                if event.key == pygame.K_DOWN:
                    assets_obj.player.speed += assets_obj.player.control_speed
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end single player")
                    assets_obj.player.reset()
                    assets_obj.opponent.reset()
                    assets_obj.ball.start()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    assets_obj.player.speed += assets_obj.player.control_speed
                if event.key == pygame.K_DOWN:
                    assets_obj.player.speed -= assets_obj.player.control_speed

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

    def local_multiplayer(self, assets_obj: assets.Assets):
        """Local multiplayer inputs handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    assets_obj.player.speed -= assets_obj.player.control_speed
                if event.key == pygame.K_DOWN:
                    assets_obj.player.speed += assets_obj.player.control_speed
                if event.key == pygame.K_w:
                    assets_obj.opponent.speed -= assets_obj.opponent.control_speed
                if event.key == pygame.K_s:
                    assets_obj.opponent.speed += assets_obj.opponent.control_speed
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end local multiplayer")
                    assets_obj.player.reset()
                    assets_obj.opponent.reset()
                    assets_obj.ball.start()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    assets_obj.player.speed += assets_obj.player.control_speed
                if event.key == pygame.K_DOWN:
                    assets_obj.player.speed -= assets_obj.player.control_speed
                if event.key == pygame.K_w:
                    assets_obj.opponent.speed += assets_obj.opponent.control_speed
                if event.key == pygame.K_s:
                    assets_obj.opponent.speed -= assets_obj.opponent.control_speed

    def client(self, assets_obj: assets.Assets, networking_obj: networking.Networking):
        """Client mode input handler"""
        assets_obj.opponent.previous_speed = assets_obj.opponent.speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    assets_obj.opponent.speed -= assets_obj.opponent.control_speed
                if event.key == pygame.K_s:
                    assets_obj.opponent.speed += assets_obj.opponent.control_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    assets_obj.opponent.speed += assets_obj.opponent.control_speed
                if event.key == pygame.K_s:
                    assets_obj.opponent.speed -= assets_obj.opponent.control_speed
                if event.key == pygame.K_ESCAPE:
                    networking_obj.is_game_running = False
                    networking_obj.network_disconnect()
                    # TODO: add network disconnect
                    self.current_menu = "title screen"
                    print("end tcp client")
                    assets_obj.player.reset()
                    assets_obj.opponent.reset()
                    assets_obj.ball.start()

            if assets_obj.opponent.speed != assets_obj.opponent.previous_speed:
                networking_obj.send_controls(assets_obj)

    def wait(self, assets_obj: assets.Assets):
        """waiting screen input handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.current_menu = "title screen"
                    print("end hosting")
                    assets_obj.player.reset()
                    assets_obj.opponent.reset()
                    assets_obj.ball.start()
                    #TODO: end hosting