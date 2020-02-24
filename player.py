from OpenGL.GL import *


class Player:
    def __init__(self, x, y, width, height, image, move_keys, name):
        self.name = name
        self.start_image = image
        self.image = 0
        self.direction = [0, 1]
        self.rect = {"x": x, "y": y, "width": width, "height": height}
        self.startpos = [x, y]
        self.walkForward = 0.01
        self.highJump = 0.05
        self.lowJump = 0.03
        self.walkCount = 0
        self.jumpCount = 0
        self.climb = False
        self.climbType = "front"
        self.health = 10
        self.move_keys = move_keys

    def draw(self):
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
        anothers = []
        for player in players:
            anothers.append(player)
        anothers.remove(self)
        if "up" not in self.touchblocks(tiles) and not self.climb:
            self.rect["y"] += self.jumpCount
            self.jumpCount -= 0.0015
        elif not self.climb:
            self.rect["y"] += 0.005
            self.jumpCount = 0
        if "down" in self.touchblocks(tiles):
            self.jumpCount = -0.01
        if "up" in self.touchblocks(anothers, climbtype=self.climbType) and not self.climb:
            self.jumpCount = self.lowJump
        if "down" in self.touchblocks(anothers, climbtype=self.climbType) and not self.climb:
            self.jumpCount = -0.01
        if self.climb and not self.touchblocks(net):
            self.climb = False
            self.jumpCount = 0
        if self.rect["y"] < -2:
            if anothers:
                self.rect["x"] = players[players.index(self) - 1].rect["x"]
                self.rect["y"] = players[players.index(self) - 1].rect["y"] + 0.2
            else:
                self.rect["x"] = self.startpos[0]
                self.rect["y"] = self.startpos[1]
            self.health -= 10
        if "up" in self.touchblocks(enemies):
            self.jumpCount = self.lowJump
        elif self.touchblocks(enemies):
            if anothers:
                self.rect["x"] = players[players.index(self) - 1].rect["x"]
                self.rect["y"] = players[players.index(self) - 1].rect["y"] + 0.2
            else:
                self.rect["x"] = self.startpos[0]
                self.rect["y"] = self.startpos[1]
            self.health -= 1
        if "up" in self.touchblocks(net_enemies, climbtype=self.climbType):
            self.jumpCount = self.lowJump
        elif self.touchblocks(net_enemies, climbtype=self.climbType):
            if anothers:
                self.rect["x"] = players[players.index(self) - 1].rect["x"]
                self.rect["y"] = players[players.index(self) - 1].rect["y"] + 0.2
            else:
                self.rect["x"] = self.startpos[0]
                self.rect["y"] = self.startpos[1]
            self.health -= 1

    def move(self, keys, tiles, net, players):
        anothers = []
        for player in players:
            anothers.append(player)
        anothers.remove(self)
        if self.move_keys[0] in keys and self.move_keys[1] not in keys:
            self.rect["x"] -= self.walkForward
            self.direction = [0, 1]
            self.walkCount += 1
            if "left" in self.touchblocks(tiles) or self.touchblocks(anothers, climbtype=self.climbType):
                self.rect["x"] += self.walkForward
        if self.move_keys[1] in keys and self.move_keys[0] not in keys:
            self.rect["x"] += self.walkForward
            self.direction = [1, 0]
            self.walkCount += 1
            if "right" in self.touchblocks(tiles) or self.touchblocks(anothers, climbtype=self.climbType):
                self.rect["x"] -= self.walkForward
        if self.move_keys[2] in keys and self.move_keys[3] not in keys and self.move_keys[5] not in keys and self.climb:
            self.rect["y"] += self.walkForward * self.rect["height"] / self.rect["width"]
            self.walkCount += 1
            if self.touchblocks(anothers, climbtype=self.climbType):
                self.rect["y"] -= self.walkForward * self.rect["height"] / self.rect["width"]
        if self.move_keys[3] in keys and self.move_keys[2] not in keys and self.move_keys[5] not in keys and self.climb:
            self.rect["y"] -= self.walkForward * self.rect["height"] / self.rect["width"]
            self.walkCount += 1
            if self.touchblocks(anothers, climbtype=self.climbType):
                self.rect["y"] += self.walkForward * self.rect["height"] / self.rect["width"]
        if self.move_keys[4] in keys and ("up" in self.touchblocks(tiles) or (self.climb and self.touchblocks(net, [0.02, 0.02]))):
            if not self.climb:
                self.jumpCount = self.highJump
                self.rect["y"] += 0.01
            else:
                self.jumpCount = self.lowJump
                self.climb = False
                self.climbType = "front"
        if self.move_keys[5] in keys and self.touchblocks(net):
            self.climb = True
            if self.move_keys[2] in keys and not self.touchblocks(anothers, climbtype="behind"):
                self.climbType = "behind"
            if self.move_keys[3] in keys and not self.touchblocks(anothers, climbtype="front"):
                self.climbType = "front"

    def touchblock(self, tile):
        if (tile.rect["x"] < self.rect["x"] + 0.02 < tile.rect["x"] + tile.rect["width"]) or (self.rect["x"] < tile.rect["x"] + 0.02 < self.rect["x"] + self.rect["width"]) or (self.rect["x"] == tile.rect["x"]):
            if (tile.rect["y"] < self.rect["y"] < tile.rect["y"] + tile.rect["height"]) or (self.rect["y"] < tile.rect["y"] < self.rect["y"] + self.rect["height"]):
                return True
        return False

    def touchblocks(self, tiles, climbtype=None):
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
