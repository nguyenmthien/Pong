"""Input for game
"""
import sys
import threading
import pygame
import assets
import networking


def game_input(assets_obj: assets.Assets,
               ui_obj: assets.UserInterface):
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
                assets_obj.reset()

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
                assets_obj.reset()

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
                networking_obj.network_disconnect(assets_obj, ui_obj)
                print("end tcp client")

        if assets_obj.opponent.speed != assets_obj.opponent.previous_speed:
            networking_obj.send_controls(assets_obj, ui_obj)


def wait_for_client(assets_obj: assets.Assets,
                    ui_obj: assets.UserInterface,
                    networking_obj: networking.Networking):
    """waiting screen input handler"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("end hosting")
                networking_obj.end_hosting(assets_obj, ui_obj)


def choose_server(assets_obj: assets.Assets,
                  ui_obj: assets.UserInterface,
                  networking_obj: networking.Networking):
    """Choose server screen input handler"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("exit game")
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if ui_obj.choice > 0:
                    ui_obj.choice -= 1
                return
            if event.key == pygame.K_DOWN:
                if ui_obj.choice < len(networking_obj.ip_result['found']):
                    ui_obj.choice += 1
                return
            if event.key == pygame.K_RETURN:
                print(f"Connect to {networking_obj.ip_result['found'][ui_obj.choice]}")
                networking_obj.connect_to_sever(
                    networking_obj.ip_result['found'][ui_obj.choice])
                return
            if event.key == pygame.K_F5:
                scan_thr = threading.Thread(target=networking_obj.scan_for_server,
                                            args=[ui_obj])
                scan_thr.start()
                return
            if event.key == pygame.K_ESCAPE:
                networking_obj.network_disconnect(assets_obj, ui_obj)
                return


def server_input(assets_obj: assets.Assets,
                 ui_obj: assets.UserInterface,
                 networking_obj: networking.Networking):
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
                print("end hosting")
                assets_obj.reset()
                networking_obj.end_hosting(assets_obj, ui_obj)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                assets_obj.player.speed += assets_obj.player.control_speed
            if event.key == pygame.K_DOWN:
                assets_obj.player.speed -= assets_obj.player.control_speed
