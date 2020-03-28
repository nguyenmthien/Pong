"""Assets animation and game logic
"""

import random
import assets
import pygame


def ball():
    """Animation and logic of ball"""

    assets.ball.x += assets.ball_speed_x
    assets.ball.y += assets.ball_speed_y

    if assets.ball.top <= 0 or assets.ball.bottom >= assets.screen_height:
        assets.ball_speed_y *= -1
    if assets.ball.left <= 0 or assets.ball.right >= assets.screen_width:
        ball_start()

    if assets.ball.colliderect(assets.player) or assets.ball.colliderect(assets.opponent):
        assets.ball_speed_x *= -1

def player():
    """Animation of player"""
    assets.player.y += assets.player_speed

    if assets.player.top <= 0:
        player.top = 0
    if assets.player.bottom >= assets.screen_height:
        player.bottom = assets.screen_height

def ball_start():
    """Replace the ball to the origin"""
    assets.ball.center = (assets.screen_width/2, assets.screen_height/2)
    assets.ball_speed_y *= random.choice((1,-1))
    assets.ball_speed_x *= random.choice((1,-1))

def opponent_ai():
    if assets.opponent.top < assets.ball.y:
        assets.opponent.y += assets.opponent_speed
    if assets.opponent.bottom > assets.ball.y:
        assets.opponent.y -= assets.opponent_speed

    if assets.opponent.top <= 0:
        assets.opponent.top = 0
    if assets.opponent.bottom >= assets.screen_height:
        assets.opponent.bottom = assets.screen_height


