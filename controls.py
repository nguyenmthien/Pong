"""Input for game
"""
import pygame
import sys
import assets
import ui

def update_input():
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
                
def input_logic():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                menu_variables.num += 1
            elif event.key==pygame.K_DOWN:
                menu_variables.num -= 1
            if event.key==pygame.K_RETURN:
                if menu_variables.selected == "SINGLE PLAYER":
                    print("start")
                if menu_variables.selected == "QUIT":
                    pygame.quit()
                    quit()  

                    