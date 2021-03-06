# Import module/files
from os import path
from player import Player
from stone import Stone
from walker import Walker
from climber import Climber
from net import Net
from tile import Tile


# Define constants
TILE_WIDTH = 0.1
TILE_HEIGHT = 0.2
CHAR_WIDTH = 0.1
CHAR_HEIGHT = 0.2


def load_map(file, move_keys, player_number):
    # Load map

    # Load background color
    f = open(path.join("levels", file + ".txt"), "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    data[0] = data[0].split(",")
    color = data[0]
    tile_chars = {}
    data.pop(0)

    # Load tiles
    while "=" in data[0]:
        tile_chars[data[0][0]] = data[0].split("=")[1].split(",")
        data.pop(0)

    # Initialize objects
    tiles = []
    net = []
    walkers = []
    climbers = []
    stones = []
    players = []

    # Load objects
    y = 1
    for row in range(len(data)):
        x = -1
        for tile in range(len(data[row])):
            if data[row][tile] in tile_chars:
                tiles.append(Tile(x, y, TILE_WIDTH, TILE_HEIGHT, tile_chars[data[row][tile]]))
            elif data[row][tile] == "p" and len(players) < player_number:
                players.append(Player(x, y, CHAR_WIDTH, CHAR_HEIGHT, 0, move_keys[len(players)]))
            elif data[row][tile] == "w":
                walkers.append(Walker(x, y, CHAR_WIDTH, CHAR_HEIGHT, 0))
            elif data[row][tile] == "n":
                net.append(Net(x, y, TILE_WIDTH, TILE_HEIGHT, 6))
            elif data[row][tile] == "c":
                net.append(Net(x, y, TILE_WIDTH, TILE_HEIGHT, 6))
                climbers.append(Climber(x, y, CHAR_WIDTH, CHAR_HEIGHT, 0))
            elif data[row][tile] == "s":
                stones.append(Stone(x, y, TILE_WIDTH, TILE_HEIGHT, 7))
            x += TILE_WIDTH
        y -= TILE_HEIGHT

    # Return objects
    return tiles, net, stones, players, walkers, climbers, color
