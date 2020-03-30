"""Main game file
"""
import assets
import animation
import controls
import ui


if __name__ == "__main__":
    ui.initialize_title_screen()
    assets.setup()
    CONTROL = controls.Control()
    while True:
        while CONTROL.current_menu == "title screen":
            CONTROL.title_screen()
            ui.main_menu()
        while CONTROL.current_menu == "single player":
            CONTROL.game_input()
            animation.ball()
            animation.player()
            animation.opponent_ai()
            assets.draw_playing_field()
        while CONTROL.current_menu == "local multiplayer":
            CONTROL.local_multiplayer()
            animation.ball()
            animation.player()
            animation.opponent()
            assets.draw_playing_field()
        while CONTROL.current_menu == "local network server":
            pass
        while CONTROL.current_menu == "local network client":
            pass
