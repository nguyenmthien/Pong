"""Main game file
"""
import assets
import animation
import controls
import ui


if __name__ == "__main__":
    ui.initialize_title_screen()
    assets.setup()
    while True:
        while controls.MENU == "title screen":
            controls.title_screen()
            ui.main_menu()
        while controls.MENU == "single player":
            controls.game_input()
            animation.ball()
            animation.player()
            animation.opponent_ai()
            assets.draw_playing_field()
        while controls.MENU == "local multiplayer":
            controls.local_multiplayer()
            animation.ball()
            animation.player()
            animation.opponent()
            assets.draw_playing_field()
