"""Main game file
"""
import assets
import controls
import networking

if __name__ == "__main__":
    UI = assets.UserInterface()
    ASSETS = assets.Assets()
    CONTROL = controls.Control()
    NET = networking.Networking()
    while True:
        while CONTROL.current_menu == "title screen":
            CONTROL.title_screen(UI)
            UI.title_screen(ASSETS)
        while CONTROL.current_menu == "single player":
            CONTROL.game_input(ASSETS)
            ASSETS.ball.animation(ASSETS.opponent, ASSETS.player)
            ASSETS.player.animation()
            ASSETS.opponent.artificial_intelligence(ASSETS.ball.rect.y)
            ASSETS.draw_playing_field()
        while CONTROL.current_menu == "local multiplayer":
            CONTROL.local_multiplayer(ASSETS)
            ASSETS.ball.animation(ASSETS.opponent, ASSETS.player)
            ASSETS.player.animation()
            ASSETS.opponent.animation()
            ASSETS.draw_playing_field()
        while CONTROL.current_menu == "local network server":
            if NET.is_binded is False:
                NET.init_server()
            if NET.is_binded is True and NET.is_game_running is False:
                NET.wait_for_client()  # UI.waiting for connection
            while NET.is_game_running is True:
                NET.send_coordinates(ASSETS)
                CONTROL.game_input(ASSETS)
                ASSETS.ball.animation(ASSETS.opponent, ASSETS.player)
                ASSETS.player.animation()
                ASSETS.opponent.animation()
                ASSETS.draw_playing_field()
                NET.send_coordinates(ASSETS)
                NET.recieve_controls(ASSETS)
        while CONTROL.current_menu == "local network client":
            if NET.is_binded is False:
                NET.init_client()
            if NET.is_binded is True and NET.is_game_running is False:
                # UI.choose_server()
                NET.connect_to_sever(networking.LOCAL_IP)
            while NET.is_game_running is True:
                CONTROL.client(ASSETS, NET)
                ASSETS.draw_client()
                NET.receive_coordinates(ASSETS)
