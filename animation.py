"""Assets animation and game logic
"""

import random
import assets
import pygame


def ball_animation():
    '''Animation and logic of ball'''
    global ball_speed_x, ball_speed_y
    
    assets.ball.x += ball_speed_x
    assets.ball.y += ball_speed_y

    if assets.ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if assets.ball.left <= 0 or ball.right >= screen_width:
        ball_start()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    assets.player.y += player_speed

    if assets.player.top <= 0:
        player.top = 0
    if assets.player.bottom >= assets.screen_height:
        player.bottom = assets.screen_height

def ball_start():
    global ball_speed_x, ball_speed_y

    assets.ball.center = (assets.screen_width/2, assets.screen_height/2)
    ball_speed_y *= random.choice((1,-1))
    ball_speed_x *= random.choice((1,-1))

def opponent_ai():
    if asets.opponent.top < assets.ball.y:
        assets.opponent.y += opponent_speed
    if assets.opponent.bottom > assets.ball.y:
        assets.opponent.y -= opponent_speed

    if assets.opponent.top <= 0:
        assets.opponent.top = 0
    if assets.opponent.bottom >= screen_height:
        assets.opponent.bottom = screen_height


