"""Main game file
"""
import threading
import assets
import controls
import networking

if __name__ == "__main__":
    UI = assets.UserInterface()
    ASSETS = assets.Assets()
    NET = networking.Networking()
    while True:
        while UI.current_menu == "TITLE SCREEN":
            controls.title_screen(UI)
            UI.title_screen(ASSETS)
        while UI.current_menu == "SINGLE PLAYER":
            controls.game_input(ASSETS, UI)
            ASSETS.ball.animation(ASSETS.opponent, ASSETS.player)
            ASSETS.player.animation()
            ASSETS.opponent.artificial_intelligence(ASSETS.ball.rect.y)
            ASSETS.draw_playing_field()
        while UI.current_menu == "LOCAL MULTIPLAYER":
            controls.local_multiplayer(ASSETS, UI)
            ASSETS.ball.animation(ASSETS.opponent, ASSETS.player)
            ASSETS.player.animation()
            ASSETS.opponent.animation()
            ASSETS.draw_playing_field()
        while UI.current_menu == "HOST GAME":
            if NET.flag['is_binded'] is False:
                NET.init_server()
            if NET.flag['is_binded'] is True and NET.flag['is_game_running'] is False:
                UI.wait_for_client(ASSETS, networking.LOCAL_IP)
                NET.wait_for_client()
                controls.wait_for_client(ASSETS, UI, NET)
            while NET.flag['is_game_running'] is True:
                controls.server_input(ASSETS, UI, NET)
                ASSETS.ball.animation(ASSETS.opponent, ASSETS.player)
                ASSETS.player.animation()
                ASSETS.opponent.animation()
                SERVER_SEND = threading.Thread(target=NET.send_coordinates, args=[ASSETS, UI])
                SERVER_SEND.start()
                NET.recieve_controls(ASSETS, UI)
                ASSETS.draw_playing_field()
        while UI.current_menu == "JOIN GAME":
            if NET.flag['is_binded'] is False:
                NET.init_client()
                SCAN_THR = threading.Thread(target=NET.scan_for_server, args=[
                    UI])
                SCAN_THR.start()
            if NET.flag['is_scanning']:
                UI.wait_for_search(ASSETS)
            if (NET.flag['is_binded'] and
                    not NET.flag['is_game_running'] and
                    not NET.flag['is_scanning']):
                UI.choose_server(ASSETS, NET.ip_result['found'])
                controls.choose_server(ASSETS, UI, NET)
            while NET.flag['is_game_running'] is True:
                ASSETS.draw_client()
                NET.receive_coordinates(ASSETS, UI)
                controls.client(ASSETS, NET, UI)
