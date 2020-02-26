from OpenGL.GL import *


class Enemy:
    def __init__(self, x, y, width, height, image):
        self.image = image
        self.direction = [0, 1]
        self.rect = {"x": x, "y": y, "width": width, "height": height}
        self.walkForward = 0.005
        self.walkCount = 0

    def draw(self):
        if self.walkCount >= 13:
            self.walkCount = 0
        glBindTexture(GL_TEXTURE_2D, self.image + self.walkCount // 7)
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

    def update(self, tiles):
        if self.direction[1]:
            self.rect["x"] -= self.walkForward
            self.walkCount += 1
        else:
            self.rect["x"] += self.walkForward
            self.walkCount += 1
        if "up" not in self.touchblocks(tiles) or "left" in self.touchblocks(tiles) or "right" in self.touchblocks(tiles):
            if self.direction[1]:
                self.direction = [1, 0]
            else:
                self.direction = [0, 1]

    def touchblock(self, tile):
        if (tile.rect["x"] < self.rect["x"] + 0.02 < tile.rect["x"] + tile.rect["width"]) or (self.rect["x"] < tile.rect["x"] + 0.02 < self.rect["x"] + self.rect["width"]) or (self.rect["x"] == tile.rect["x"]):
            if self.rect["y"] == tile.rect["y"] + tile.rect["height"] or self.rect["y"] == tile.rect["y"]:
                return True
        return False

    def touchblocks(self, tiles):
        touchtiles = []
        touches = []
        for tile in tiles:
            if self.touchblock(tile):
                touchtiles.append(tile)
        for tile in touchtiles:
            if abs(self.rect["y"] - tile.rect["y"]) > abs(self.rect["x"] - tile.rect["x"]):
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