"""Input for game
"""
import sys
import pygame
import assets
import networking


def game_input(assets_obj: assets.Assets, ui_obj: assets.UserInterface):
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
                ui_obj.current_menu = "TITLE SCREEN"
                print("end single player")
                assets_obj.player.reset()
                assets_obj.opponent.reset()
                assets_obj.ball.start()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                assets_obj.player.speed += assets_obj.player.control_speed
            if event.key == pygame.K_DOWN:
                assets_obj.player.speed -= assets_obj.player.control_speed


def title_screen(ui_obj: assets.UserInterface):
    """Title screen input handler"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("exit game")
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if ui_obj.choice > 0:
                    ui_obj.choice -= 1
            elif event.key == pygame.K_DOWN:
                if ui_obj.choice < len(ui_obj.selection_list):
                    ui_obj.choice += 1
            if event.key == pygame.K_RETURN:
                if ui_obj.selection_list[ui_obj.choice] == "QUIT":
                    print("exit game")
                    pygame.quit()
                    sys.exit()
                else:
                    print(ui_obj.selection_list[ui_obj.choice])
                    ui_obj.current_menu = ui_obj.selection_list[ui_obj.choice]


def local_multiplayer(assets_obj: assets.Assets, ui_obj: assets.UserInterface):
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
                ui_obj.current_menu = "TITLE SCREEN"
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


def client(assets_obj: assets.Assets,
           networking_obj: networking.Networking,
           ui_obj: assets.UserInterface):
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
                ui_obj.current_menu = "TITLE SCREEN"
                print("end tcp client")
                assets_obj.player.reset()
                assets_obj.opponent.reset()
                assets_obj.ball.start()

        if assets_obj.opponent.speed != assets_obj.opponent.previous_speed:
            networking_obj.send_controls(assets_obj)


def wait(assets_obj: assets.Assets, ui_obj: assets.UserInterface):
    """waiting screen input handler"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ui_obj.current_menu = "TITLE SCREEN"
                print("end hosting")
                assets_obj.player.reset()
                assets_obj.opponent.reset()
                assets_obj.ball.start()
                #TODO: end hosting
