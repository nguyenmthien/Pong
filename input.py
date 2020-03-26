"""Input for game
"""
import pygame
import assets

def update_input():
    """Update pygame events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                assets.player_speed -= 6
            if event.key == pygame.K_DOWN:
                assets.player_speed += 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                assets.player_speed += 6
            if event.key == pygame.K_DOWN:
                assets.player_speed -= 6