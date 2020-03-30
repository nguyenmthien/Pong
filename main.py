"""Main game file
"""
import assets
import controls
import ui


if __name__ == "__main__":
    UI = ui.UserInterface()
    ASSETS = assets.Assets()
    CONTROL = controls.Control()
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
            CONTROL.game_input(ASSETS)
            ASSETS.ball.animation(ASSETS.opponent, ASSETS.player)
            ASSETS.player.animation()
            ASSETS.opponent.animation()
            ASSETS.draw_playing_field()
            #missing functions
        while CONTROL.current_menu == "local network client":
            CONTROL.client(ASSETS)
            ASSETS.draw_client()
            #missing function
            