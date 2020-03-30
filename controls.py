"""Input for game
"""
import sys
import pygame
import assets
import ui
import animation


MENU = "title screen"


def game_input():
    """Singleplayer input handler"""
    global MENU

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                assets.player_speed -= assets.player_control_speed
            if event.key == pygame.K_DOWN:
                assets.player_speed += assets.player_control_speed
            if event.key == pygame.K_ESCAPE:
                MENU = "title screen"
                print("end single player")
                animation.reset()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                assets.player_speed += assets.player_control_speed
            if event.key == pygame.K_DOWN:
                assets.player_speed -= assets.player_control_speed


def title_screen():
    """Title screen input handler"""
    global MENU
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if ui.choice > 0:
                    ui.choice -= 1
            elif event.key == pygame.K_DOWN:
                if ui.choice < 3:
                    ui.choice += 1
            if event.key == pygame.K_RETURN:
                if ui.selection_list[ui.choice] == "SINGLE PLAYER":
                    print("start single player")
                    MENU = "single player"
                if ui.selection_list[ui.choice] == "LOCAL MULTIPLAYER":
                    print("start single player")
                    MENU = "local multiplayer"
                if ui.selection_list[ui.choice] == "QUIT":
                    pygame.quit()
                    sys.exit()


def local_multiplayer():
    """Local multiplayer inputs handler"""
    global MENU
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                assets.player_speed -= assets.player_control_speed
            if event.key == pygame.K_DOWN:
                assets.player_speed += assets.player_control_speed
            if event.key == pygame.K_w:
                assets.opponent_speed -= assets.opponent_control_speed
            if event.key == pygame.K_s:
                assets.opponent_speed += assets.opponent_control_speed
            if event.key == pygame.K_ESCAPE:
                MENU = "title screen"
                print("end local multiplayer")
                animation.reset()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                assets.player_speed += assets.player_control_speed
            if event.key == pygame.K_DOWN:
                assets.player_speed -= assets.player_control_speed
            if event.key == pygame.K_w:
                assets.opponent_speed += assets.opponent_control_speed
            if event.key == pygame.K_s:
                assets.opponent_speed -= assets.opponent_control_speed
