# Import mudules/packages/files
from load_map import load_map
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from time import sleep
from sys import exit
from os import path
import numpy as np


# Define variables

# Set number of players
player_number = "1"
player_number = int(player_number)
if player_number < 1:
    player_number = 1
elif player_number > 3:
    player_number = 3

# Define lists
scroll = [1, 0]
move_keys = ((100, 102, 101, 103, b"x", b"z"), (b"a", b"d", b"w", b"s", b"q", b"e"))
keys = []

# Open textures
texture = [0, 1, 2, 3, 4, 5, 6, 7]
char_imgs = [path.join("images", "walk1.png"), path.join("images", "walk2.png"), path.join("images", "front1.png"), path.join("images", "front2.png"), path.join("images", "behind1.png"), path.join("images", "behind2.png")]
net_img = path.join("images", "net.png")
stone_img = path.join("images", "stone.png")

# Load screen
tiles, net, stones, players, enemies, net_enemies, color = load_map("first", move_keys, player_number)
for i in range(len(color)):
    color[i] = float(color[i])


def main():
    # Clear screen
    glClearColor(color[0], color[1], color[2], 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw screen

    # Set camera position
    for player in players:
        scroll[0] += player.rect["x"]
        scroll[1] += player.rect["y"]
    scroll[0] /= len(players)
    scroll[1] /= len(players)
    gluLookAt(scroll[0], scroll[1], 1, scroll[0], scroll[1], 0, 0, 1, 0)
    scroll[0] = 0
    scroll[1] = 0

    # Draw tiles
    for tile in tiles:
        tile.draw()

    # Draw players behind net
    for i in range(len(players)):
        if players[i].climbType == "behind":
            players[i].draw()

    # Draw climbers behind net
    for net_enemy in net_enemies:
        if net_enemy.climbType == "behind":
            net_enemy.draw()

    # Draw net
    for string in net:
        string.draw()

    # Draw stones
    for stone in stones:
        stone.draw()
        stone.update(tiles)

    # Draw players in front of net, update players and move players
    for player in players:
        try:
            if player.climbType == "front":
                player.draw()
            player.move(keys, tiles, net, net_enemies, stones, players)
            player.update(tiles, net, players, enemies, net_enemies)
            if not player.health:
                players.remove(player)
        except IndexError:
            pass
        if not players:
            glutDestroyWindow(window)
            exit()

    # Draw walkers and update walkers
    for enemy in enemies:
        try:
            enemy.draw()
            enemy.update(tiles, stones)
            if not enemy.health:
                enemies.remove(enemy)
        except IndexError:
            pass

    # Draw climbers in front of net and update climbers
    for net_enemy in net_enemies:
        try:
            if net_enemy.climbType == "front":
                net_enemy.draw()
            net_enemy.update(net, stones)
            if not net_enemy.health:
                net_enemies.remove(net_enemy)
        except IndexError:
            pass

    # Show on screen
    glutSwapBuffers()
    sleep(0.01)


def specialdown(key, x, y):
    # Add key to keypresses
    if key not in keys:
        keys.append(key)


def specialup(key, x, y):
    # Remove key from keypresses
    try:
        keys.remove(key)
    except ValueError:
        pass


def keyboarddown(key, x, y):
    # Exit window when Escape key is pressed
    if key == b'\x1b':
        glutDestroyWindow(window)
        exit()

    # Add key to keypresses
    elif key not in keys:
        keys.append(key)


def keyboardup(key, x, y):
    # Remove key from keypresses
    try:
        keys.remove(key)
    except ValueError:
        pass


# Setup window
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA)
glutInitWindowSize(600, 600)
glutInitWindowPosition(400, 400)
window = glutCreateWindow("Platformer")


# Start functions
glutIdleFunc(main)
glutSpecialFunc(specialdown)
glutSpecialUpFunc(specialup)
glutKeyboardFunc(keyboarddown)
glutKeyboardUpFunc(keyboardup)


# Load textures
glEnable(GL_ALPHA_TEST)
glAlphaFunc(GL_GREATER, 0.8)
glGenTextures(len(texture), texture)

# Load character images
for char_img in range(len(char_imgs)):
    char_imgs[char_img] = Image.open(char_imgs[char_img]).getdata()
    glBindTexture(GL_TEXTURE_2D, char_img)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, char_imgs[char_img].size[0], char_imgs[char_img].size[1], 0, GL_RGBA, GL_FLOAT, np.array(char_imgs[char_img]).reshape([char_imgs[char_img].size[0], char_imgs[char_img].size[1], 4]) / 256)

# Load net image
net_img = Image.open(net_img).getdata()
glBindTexture(GL_TEXTURE_2D, 6)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, net_img.size[0], net_img.size[1], 0, GL_RGBA, GL_FLOAT, np.array(net_img).reshape([net_img.size[0], net_img.size[1], 4]) / 256)

# Load stone image
stone_img = Image.open(stone_img).getdata()
glBindTexture(GL_TEXTURE_2D, 7)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, stone_img.size[0], stone_img.size[1], 0, GL_RGBA, GL_FLOAT, np.array(stone_img).reshape([stone_img.size[0], stone_img.size[1], 4]) / 256)


# Open window
glutFullScreen()
glutMainLoop()
