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
    if assets.ball.colliderect(assets.opponent) or assets.ball.colliderect(assets.player):
        assets.ball_speed_x *= -1

    if  assets.ball.right >= assets.screen_width:
        ball_start()
        score("opponent")

    if assets.ball.left <= 0:
        ball_start()
        score("player")


def ball_start():
    """Replace the ball to the origin"""
    assets.ball.center = (assets.screen_width/2, assets.screen_height/2)
    assets.ball_speed_y *= random.choice((1,-1))
    assets.ball_speed_x *= random.choice((1,-1))


def player():
    """Animation of player"""
    assets.player.y += assets.player_speed

    if assets.player.top <= 0:
        assets.player.top = 0
    if assets.player.bottom >= assets.screen_height:
        assets.player.bottom = assets.screen_height


def opponent_ai():
    """Single-player AI"""
    if assets.opponent.top < assets.ball.y:
        assets.opponent.y += assets.opponent_ai_speed
    if assets.opponent.bottom > assets.ball.y:
        assets.opponent.y -= assets.opponent_ai_speed

    if assets.opponent.top <= 0:
        assets.opponent.top = 0
    if assets.opponent.bottom >= assets.screen_height:
        assets.opponent.bottom = assets.screen_height


def score(person):
    if person == "opponent":
        assets.opponent_score_value += 1
        assets.opponent_score = assets.display_font.render(str(assets.opponent_score_value), 1, assets.Color.light_grey)
    if person == "player":
        assets.player_score_value += 1
        assets.player_score = assets.display_font.render(str(assets.player_score_value), 1, assets.Color.light_grey)
