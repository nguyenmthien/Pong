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
            if NET.is_binded is False:
                NET.init_server()
            if NET.is_binded is True and NET.is_game_running is False:
                UI.wait_for_client(ASSETS, networking.LOCAL_IP)
                NET.wait_for_client()
            while NET.is_game_running is True:
                controls.game_input(ASSETS, UI)
                ASSETS.ball.animation(ASSETS.opponent, ASSETS.player)
                ASSETS.player.animation()
                ASSETS.opponent.animation()
                SERVER_SEND = threading.Thread(target=NET.send_coordinates(ASSETS))
                NET.recieve_controls(ASSETS)
                ASSETS.draw_playing_field()
        while UI.current_menu == "JOIN GAME":
            if NET.is_binded is False:
                NET.init_client()
            if NET.is_binded is True and NET.is_game_running is False:
                # UI.choose_server()
                NET.connect_to_sever(networking.LOCAL_IP)
            while NET.is_game_running is True:
                ASSETS.draw_client()
                NET.receive_coordinates(ASSETS)
                controls.client(ASSETS, NET, UI)
