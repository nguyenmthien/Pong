"""Main game file
"""

import pygame
import assets
import animation
import input

if __name__ == "__main__":
    assets.setup()
    assets.draw_playing_field()
    while True:
        input.update_input()
        animation.ball()
        animation.player()
        animation.opponent_ai()
        assets.draw_playing_field()