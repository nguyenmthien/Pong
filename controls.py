"""Input for game
"""
import pygame
import sys
import assets
import ui


menu = "title screen"
def game_input():
    """Update pygame events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                assets.player_speed -= assets.player_control_speed
            if event.key == pygame.K_DOWN:
                assets.player_speed += assets.player_control_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                assets.player_speed += assets.player_control_speed
            if event.key == pygame.K_DOWN:
                assets.player_speed -= assets.player_control_speed


def title_screen():
    global menu
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                if ui.choice > 0:
                    ui.choice -= 1
            elif event.key==pygame.K_DOWN:
                if ui.choice < 3:
                    ui.choice += 1
            if event.key==pygame.K_RETURN:
                if ui.selection_list[ui.choice]== "SINGLE PLAYER":
                    print("start")
                    menu = "single player"
                if ui.selection_list[ui.choice] == "QUIT":
                    pygame.quit()
                    quit()  
        break
