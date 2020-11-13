"""
reza barzgar code 1
9622762384
"""

import random
import socket
import pickle
import pygame

Bytes = 2048
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 8818))
server_socket.listen(2)
clock = pygame.time.Clock()

positions = [180, 180, 350, 250, 0, 0, True]
connections = []
ball_speed_x = -1
ball_speed_y = -1

ball_rand_speed = [1, -1]
"""
positions[0] = player 1 y
positions[1] = player 2 y
positions[2] = ball x
positions[3] = ball y
positions[4] = player1 points
positions[5] = player2 points
positions[6] = if false --> running false ,if true --> running true 

"""


def update_positions(data):
    """

    :param data: [0] key up - [1] key down - [2]stop - [3]restart
    :param data: [0] key up - [1] key down - [2]stop - [3]restart
    :return: NONE
    """
    global positions, ball_speed_x, ball_speed_y

    if data[0][3] or data[1][3]:
        positions = [180, 180, 350, 250, 0, 0, True, False]
        return

    if data[0][2] or data[1][2]:
        return

        # player move
    if data[0][0]:
        positions[0] -= 1
    if data[0][1]:
        positions[0] += 1
    if data[1][0]:
        positions[1] -= 1
    if data[1][1]:
        positions[1] += 1

    if positions[0] <= 40:
        positions[0] = 40
    if positions[0] >= 390:
        positions[0] = 390
    if positions[1] <= 40:
        positions[1] = 40
    if positions[1] >= 390:
        positions[1] = 390

    # ball move
    positions[2] += ball_speed_x
    positions[3] += ball_speed_y
    print(positions[3])
    if (positions[3] == 50) or (positions[3] == 450):
        ball_speed_y = -ball_speed_y

    if positions[2] == 30 and (positions[3] >= positions[0] and positions[3] <= positions[0] + 70):
        ball_speed_x = -ball_speed_x

    elif positions[2] == 0:
        if positions[5] + 1 < 3:
            ball_speed_x = random.choice(ball_rand_speed)
            ball_speed_y = random.choice(ball_rand_speed)
            positions = [180, 180, 350, 250, positions[4], positions[5] + 1, True]
        else:
            positions = [180, 180, 350, 250, positions[4], positions[5] + 1, False]

    if positions[2] == 670 and (positions[3] >= positions[1] and positions[3] <= positions[1] + 70):
        ball_speed_x = -ball_speed_x

    if positions[2] == 700:
        if positions[4] + 1 < 3:
            ball_speed_x = random.choice(ball_rand_speed)
            ball_speed_y = random.choice(ball_rand_speed)
            positions = [180, 180, 350, 250, positions[4] + 1, positions[5], True]
        else:
            positions = [180, 180, 350, 250, positions[4] + 1, positions[5], False]
    print(str(positions[4]) + " " + str(positions[5]))


def wait_for_connections():
    while len(connections) < 2:
        connection, addr = server_socket.accept()
        connections.append(connection)
        print(addr)


def get_clients_data():
    data = []
    player1 = connections[0].recv(Bytes)
    player1 = pickle.loads(player1)
    player2 = pickle.loads(connections[1].recv(Bytes))
    data.append(player1)
    data.append(player2)
    return data


while True:
    wait_for_connections()

    pickled_data = pickle.dumps(positions)
    connections[0].send(pickled_data)
    connections[1].send(pickled_data)
    clock.tick(120)
    players_data = get_clients_data()
    print(players_data)
    update_positions(players_data)
