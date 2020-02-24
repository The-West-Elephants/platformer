from load_map import load_map
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from time import sleep
from sys import exit
import numpy as np

TILE_WIDTH = 0.1
TILE_HEIGHT = 0.2

player_number = "1"
player_number = int(player_number)
if player_number < 1:
    player_number = 1
elif player_number > 3:
    player_number = 3

scroll = [1, 0]
move_keys = ((100, 102, 101, 103, b"x", b"z"), (b"a", b"d", b"w", b"s", b"q", b"e"))
keys = []
texture = [0, 1, 2, 3, 4, 5, 6]
texture_data = ["images/char11.png", "images/char12.png", "images/char13.png", "images/char14.png", "images/char15.png", "images/char16.png", "images/net.png"]

tiles, net, players, enemies, net_enemies, color = load_map("first", move_keys, player_number)
for i in range(len(color)):
    color[i] = float(color[i])


def main():
    glClearColor(color[0], color[1], color[2], 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    for player in players:
        scroll[0] += player.rect["x"]
        scroll[1] += player.rect["y"]
    scroll[0] /= len(players)
    scroll[1] /= len(players)
    gluLookAt(scroll[0], scroll[1], 1, scroll[0], scroll[1], 0, 0, 1, 0)
    scroll[0] = 0
    scroll[1] = 0
    for tile in tiles:
        tile.draw()
    for i in range(len(players)):
        if players[i].climbType == "behind":
            players[i].draw()
    for net_enemy in net_enemies:
        if net_enemy.climbType == "behind":
            net_enemy.draw()
    for string in net:
        string.draw()
    for i in range(len(players)):
        try:
            if players[i].climbType == "front":
                players[i].draw()
            players[i].move(keys, tiles, net, players)
            players[i].update(tiles, net, players, enemies, net_enemies)
            if not players[i].health:
                del players[i]
        except IndexError:
            pass
        if not players:
            glutDestroyWindow(window)
            exit()
    for enemy in enemies:
        enemy.draw()
        enemy.update(tiles)
    for net_enemy in net_enemies:
        if net_enemy.climbType == "front":
            net_enemy.draw()
        net_enemy.update(net)
    glutSwapBuffers()
    sleep(0.01)


def specialdown(key, x, y):
    if key not in keys:
        keys.append(key)


def specialup(key, x, y):
    try:
        keys.remove(key)
    except ValueError:
        pass


def keyboarddown(key, x, y):
    if key == b'\x1b':
        glutDestroyWindow(window)
        exit()
    elif key not in keys:
        keys.append(key)


def keyboardup(key, x, y):
    try:
        keys.remove(key)
    except ValueError:
        pass


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA)
glutInitWindowSize(600, 600)
glutInitWindowPosition(400, 400)
window = glutCreateWindow("Platformer")
glEnable(GL_ALPHA_TEST)
glAlphaFunc(GL_GREATER, 0.5)
glutIdleFunc(main)
glutSpecialFunc(specialdown)
glutSpecialUpFunc(specialup)
glutKeyboardFunc(keyboarddown)
glutKeyboardUpFunc(keyboardup)
glGenTextures(len(texture), texture)
for texture_index in texture:
    texture_data[texture_index] = Image.open(texture_data[texture_index]).getdata()
    glBindTexture(GL_TEXTURE_2D, texture_index)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_data[texture_index].size[0], texture_data[texture_index].size[1], 0, GL_RGBA, GL_FLOAT, np.array(texture_data[texture_index]).reshape([texture_data[texture_index].size[0], texture_data[texture_index].size[1], 4]) / 256)
glutFullScreen()
glutMainLoop()
