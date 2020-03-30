"""Assets animation and game logic
"""

import random
import assets


def ball():
    """Animation and logic of ball"""
    ball_change_position()
    ball_wall_check_collision()
    ball_paddle_check_collision()


def ball_start():
    """Replace the ball to the origin"""
    assets.ball.center = (assets.screen_width/2, assets.screen_height/2)
    assets.ball_speed_y = assets.ball_speed_y_initial*random.choice((1, -1))
    assets.ball_speed_x *= random.choice((1, -1))


def ball_change_position():
    """Update position of ball"""
    assets.ball.x += assets.ball_speed_x
    assets.ball.y += assets.ball_speed_y


def ball_wall_check_collision():
    """Check colision and change movement of ball with wall"""

    if  assets.ball.right >= assets.screen_width:
        ball_start()
        score("opponent")

    if assets.ball.left <= 0:
        ball_start()
        score("player")

    if assets.ball.top <= 0 or assets.ball.bottom >= assets.screen_height:
        assets.ball_speed_y *= -1

def ball_paddle_check_collision():
    """Check colision and change movement of ball with paddles"""
    if assets.ball.colliderect(assets.opponent):
        assets.ball_speed_x *= -1
        assets.ball_speed_y = int((assets.ball.centery - assets.opponent.centery)/4)

    if assets.ball.colliderect(assets.player):
        assets.ball_speed_x *= -1
        assets.ball_speed_y = int((assets.ball.centery - assets.player.centery)
                                  *assets.ball_speed_y_modifier)


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


def opponent():
    """Local multiplayer opponent animation"""
    assets.opponent.y += assets.opponent_speed

    if assets.opponent.top <= 0:
        assets.opponent.top = 0
    if assets.opponent.bottom >= assets.screen_height:
        assets.opponent.bottom = assets.screen_height


def score(person):
    """Update and draw score of players"""
    if person == "opponent":
        assets.opponent_score_value += 1
        assets.opponent_score = assets.display_font.render(str(assets.opponent_score_value),
                                                           1,
                                                           assets.Color.light_grey)
    if person == "player":
        assets.player_score_value += 1
        assets.player_score = assets.display_font.render(str(assets.player_score_value),
                                                         1,
                                                         assets.Color.light_grey)


def reset():
    """Reset everything to its initial position"""
    ball_start()
    assets.player_score_value = 0
    assets.opponent_score_value = 0
    assets.player.centery = int(assets.screen_height/2)
    assets.opponent.centery = int(assets.screen_height/2)
