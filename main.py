"""Main game file
"""
import pygame
import assets
import animation
import controls
import ui

if __name__ == "__main__":
    ui.initialize_menu()
    ui.initialize_title_screen()
    assets.setup()
    while True:
        while controls.menu == "title screen":
            controls.title_screen()
            ui.main_menu()
        while controls.menu == "single player":
            controls.game_input()
            animation.ball()
            animation.player()
            animation.opponent_ai()
            assets.draw_playing_field()
        
