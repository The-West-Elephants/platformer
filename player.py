# Import package
from OpenGL.GL import *


class Player:
    # Define constants
    HIGH_JUMP = 0.05
    MID_JUMP = 0.04
    LOW_JUMP = 0.035

    def __init__(self, x, y, width, height, image, move_keys):
        # Define variables
        self.start_image = image
        self.image = 0
        self.direction = [0, 1]
        self.rect = {"x": x, "y": y, "width": width, "height": height}
        self.walkForward = 0.01
        self.walkCount = 0
        self.jumpCount = 0
        self.climb = False
        self.climbType = "front"
        self.holding = None
        self.health = 10
        self.move_keys = move_keys

    def draw(self):
        # Draw player
        if self.climb:
            self.image = 2
            self.direction = [0, 1]
            if self.climbType == "behind":
                self.image = 4
        else:
            self.image = 0
            self.climbType = "front"
        if self.walkCount >= 13:
            self.walkCount = 0
        glBindTexture(GL_TEXTURE_2D, self.start_image + self.image + self.walkCount // 7)
        glEnable(GL_TEXTURE_2D)
        glTranslate(self.rect["x"], self.rect["y"], 0)
        glBegin(GL_QUAD_STRIP)
        glTexCoord2f(self.direction[0], 1)
        glVertex2f(0, 0)
        glTexCoord2f(self.direction[1], 1)
        glVertex2f(self.rect["width"], 0)
        glTexCoord2f(self.direction[0], 0)
        glVertex2f(0, self.rect["height"])
        glTexCoord2f(self.direction[1], 0)
        glVertex2f(self.rect["width"], self.rect["height"])
        glEnd()
        glTranslate(-self.rect["x"], -self.rect["y"], 0)
        glDisable(GL_TEXTURE_2D)

    def update(self, tiles, net, players, enemies, net_enemies):
        # Load other players
        anothers = []
        for player in players:
            anothers.append(player)
        anothers.remove(self)

        # Gravitation
        if "up" not in self.touchblocks(tiles) and not self.climb:
            self.rect["y"] += self.jumpCount
            self.jumpCount -= 0.0015
        elif not self.climb:
            self.rect["y"] += 0.005
            self.jumpCount = 0

        # Fall when touch bottom of a tile
        if "down" in self.touchblocks(tiles):
            self.jumpCount = -0.01

        # Jump when touch top of a player
        if "up" in self.touchblocks(anothers, climbtype=self.climbType):
            self.jumpCount = self.MID_JUMP
            self.climb = False

        # Fall when touch bottom of a player
        if "down" in self.touchblocks(anothers, climbtype=self.climbType):
            self.jumpCount = -0.01
            self.climb = False

        # Stop climbing when don't touch net
        if self.climb and not self.touchblocks(net):
            self.climb = False
            self.jumpCount = 0

        # Die when fall to the bottom position
        if self.rect["y"] < -2:
            if self.holding:
                self.holding.rect["y"] = self.rect["y"]
                self.holding.holding = None
                self.holding = None
            self.health = 0

        # Jump when touch top of a walker
        if "up" in self.touchblocks(enemies):
            self.jumpCount = self.MID_JUMP

        # Die when touch a walker from left or right
        elif self.touchblocks(enemies):
            if self.holding:
                self.holding.rect["y"] = self.rect["y"]
                self.holding.holding = None
                self.holding = None
            self.health = 0

        # Jump when touch top of a climber
        if "up" in self.touchblocks(net_enemies, climbtype=self.climbType):
            self.jumpCount = self.MID_JUMP

        # Die when touch a climber from left or right
        elif self.touchblocks(net_enemies, climbtype=self.climbType):
            if self.holding:
                self.holding.rect["y"] = self.rect["y"]
                self.holding.holding = None
                self.holding = None
            self.health = 0

    def move(self, keys, tiles, net, net_enemies, stones, players):
        # Load other players
        anothers = []
        for player in players:
            anothers.append(player)
        anothers.remove(self)

        # Move left
        if self.move_keys[0] in keys and self.move_keys[1] not in keys:
            self.rect["x"] -= self.walkForward
            self.direction = [0, 1]
            self.walkCount += 1
            if "left" in self.touchblocks(tiles) or self.touchblocks(anothers, climbtype=self.climbType):
                self.rect["x"] += self.walkForward
            if self.holding:
                self.holding.direction = -1

        # Move right
        if self.move_keys[1] in keys and self.move_keys[0] not in keys:
            self.rect["x"] += self.walkForward
            self.direction = [1, 0]
            self.walkCount += 1
            if "right" in self.touchblocks(tiles) or self.touchblocks(anothers, climbtype=self.climbType):
                self.rect["x"] -= self.walkForward
            if self.holding:
                self.holding.direction = 1

        # Climb up
        if self.move_keys[2] in keys and self.move_keys[3] not in keys and self.move_keys[5] not in keys and self.climb:
            self.rect["y"] += self.walkForward * self.rect["height"] / self.rect["width"]
            self.walkCount += 1
            if self.touchblocks(anothers, climbtype=self.climbType):
                self.rect["y"] -= self.walkForward * self.rect["height"] / self.rect["width"]

        # Climb down
        if self.move_keys[3] in keys and self.move_keys[2] not in keys and self.move_keys[5] not in keys and self.climb:
            self.rect["y"] -= self.walkForward * self.rect["height"] / self.rect["width"]
            self.walkCount += 1
            if self.touchblocks(anothers, climbtype=self.climbType):
                self.rect["y"] += self.walkForward * self.rect["height"] / self.rect["width"]

        # Jump
        if self.move_keys[4] in keys and ("up" in self.touchblocks(tiles) or self.climb):
            if not self.climb:
                if self.move_keys[2] in keys:
                    self.jumpCount = self.HIGH_JUMP
                elif self.move_keys[3] in keys:
                    self.jumpCount = self.LOW_JUMP
                else:
                    self.jumpCount = self.MID_JUMP
                self.rect["y"] += 0.01
            else:
                self.jumpCount = self.MID_JUMP
                self.climb = False
                self.climbType = "front"

        # Climb
        if self.move_keys[5] in keys and self.touchblocks(net) and not self.holding:
            self.climb = True
            if self.move_keys[2] in keys and not self.touchblocks(anothers, climbtype="behind") and not self.touchblocks(net_enemies, climbtype="behind"):
                self.climbType = "behind"
            if self.move_keys[3] in keys and not self.touchblocks(anothers, climbtype="front") and not self.touchblocks(net_enemies, climbtype="front"):
                self.climbType = "front"

        # Pickup a stone
        elif self.move_keys[5] in keys and self.move_keys[3] in keys:
            for stone in stones:
                if self.touchblock(stone) and not self.holding:
                    self.holding = stone
                    self.holding.holding = self

        # Throw a stone
        elif self.move_keys[5] in keys and self.move_keys[2] in keys and self.holding:
            self.holding.throwing = True
            self.holding.rect["y"] = self.rect["y"]
            self.holding.forward = 0.03
            self.holding.holding = None
            self.holding = None

    def touchblock(self, tile):
        # Check for player touch an object
        if (tile.rect["x"] < self.rect["x"] + 0.02 < tile.rect["x"] + tile.rect["width"]) or (self.rect["x"] < tile.rect["x"] + 0.02 < self.rect["x"] + self.rect["width"]) or (self.rect["x"] == tile.rect["x"]):
            if (tile.rect["y"] < self.rect["y"] < tile.rect["y"] + tile.rect["height"]) or (self.rect["y"] < tile.rect["y"] < self.rect["y"] + self.rect["height"]):
                return True
        return False

    def touchblocks(self, tiles, climbtype=None):
        # Find directions that player touch
        touchtiles = []
        touches = []
        for tile in tiles:
            try:
                if climbtype == tile.climbType:
                    if self.touchblock(tile):
                        touchtiles.append(tile)
            except AttributeError:
                if self.touchblock(tile):
                    touchtiles.append(tile)
        for tile in touchtiles:
            if abs(self.rect["y"] - tile.rect["y"]) - 0.1 > abs(self.rect["x"] - tile.rect["x"]):
                if self.rect["y"] > tile.rect["y"]:
                    touches.append("up")
                else:
                    touches.append("down")
            else:
                if self.rect["x"] > tile.rect["x"]:
                    touches.append("left")
                else:
                    touches.append("right")
        return touches
