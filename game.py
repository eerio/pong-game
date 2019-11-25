import pygame

from gameobjects import GameObject
from mathutil import Point, Vector, Circle, Rect, overlap, reflect_by_rect
from colors import *

FPS = 60

# init pygame
pygame.init()
clock = pygame.time.Clock()

# init screen and window
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ping-pong")

PAD_ALIGN = 0.2 * SCREEN_WIDTH
PAD_WIDTH = 25
PAD_HEIGHT = 150

ball = GameObject(
    body = Circle(
        init_pos=Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        r=25),
    init_v = Vector(8, 0))

left_pad = GameObject(
    body = Rect(
        init_pos=Point(PAD_ALIGN, 0),
        width=PAD_WIDTH,
        height=PAD_HEIGHT),
    init_v = Vector(0, 0))

right_pad = GameObject(
    body = Rect(
        Point(SCREEN_WIDTH - PAD_ALIGN, SCREEN_HEIGHT),
        width=PAD_WIDTH,
        height=PAD_HEIGHT),
    init_v = Vector(0, 0))

game_ended = False

while not game_ended:
    # collect the input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_ended = True
        elif event.type == pygame.KEYUP and event.dict['key'] == pygame.K_ESCAPE:
            game_ended = True
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # update game objects' positions
    left_pad.body.pos.y = mouse_y
    right_pad.body.pos.y = mouse_y
    ball.body.pos += ball.v

    # redraw the screen content
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, left_pad.body.get_pygame_rect())
    pygame.draw.rect(screen, RED, right_pad.body.get_pygame_rect())
    pygame.draw.circle(screen, BLUE, ball.body.pos.to_tuple(), int(ball.body.r))
    pygame.display.flip()

    # which side of the board is the ball on?
    half = int(ball.body.pos.x) // (SCREEN_WIDTH // 2)

    # Detect collision
    pad = [left_pad, right_pad][half]

    if overlap(ball.body, pad.body):
        reflect_by_rect(ball, pad)

    clock.tick(FPS)

pygame.quit()
