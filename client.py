"""
reza barzgar code 1
9622762384
"""

import socket
import pickle
import time

import pygame

Bytes = 2048
RED = (214, 40, 40)
ORANGE = (247, 127, 0)
BALL_COLOR = (234, 226, 183)
BACKGROUND = (0, 39, 73)

pygame.init()
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("PONG!")
clock = pygame.time.Clock()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 8818))


def get_data():
    data = client_socket.recv(Bytes)
    return pickle.loads(data)

def draw_player(x, y, player_number):
    if player_number == 0:
        pygame.draw.rect(screen, RED, [x, y, 10, 70])
    if player_number == 1:
        pygame.draw.rect(screen, ORANGE, [x, y, 10, 70])

    pygame.draw.line(screen, BALL_COLOR, (0, 40), (700, 40))
    pygame.draw.line(screen, BALL_COLOR, (0, 460), (700, 460))


def ball_draw(x, y):
    pygame.draw.circle(screen, BALL_COLOR, [x, y], 10)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def message_display(text, x, y):
    largeText = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)


def display():
    running = True
    up = 0
    down = 0
    data = [False, False, False, False]
    stop = False
    while running:
        restart = False
        positions = get_data()
        clock.tick(120)
        if not positions[6]:
            running = False
            if positions[4] == 3:
                finish(1)
            else:
                finish(2)
        """
        positions[0] = player 1 y
        positions[1] = player 2 y
        positions[2] = ball x
        positions[3] = ball y
        positions[4] = player1 points
        positions[5] = player2 points
        positions[6] = if 0 --> running false if 1 --> running true 
        """
        screen.fill(BACKGROUND)
        draw_player(10, positions[0], 0)
        draw_player(680, positions[1], 1)
        ball_draw(positions[2], positions[3])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up = 1
                if event.key == pygame.K_DOWN:
                    down = 1
                if event.key == pygame.K_s:
                    stop = not stop
                if event.key == pygame.K_r:
                    restart = True
                if event.key == pygame.K_x:
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = 0
                if event.key == pygame.K_DOWN:
                    down = 0

        message_display("player 1 = {}".format(positions[4]), 100, 20)
        message_display("player 2 = {}".format(positions[5]), 600, 20)
        pygame.display.update()
        if up == 1:
            data[0] = True
        else:
            data[0] = False
        if down == 1:
            data[1] = True
        else:
            data[1] = False
        data[2] = stop
        data[3] = restart
        """
        data[0] = up
        """
        client_socket.sendall(pickle.dumps(data))


def finish(number):
    screen.fill(BACKGROUND)
    message_display("player {} has won the game!".format(number), 350, 250)
    pygame.display.update()
    time.sleep(2)


display()
