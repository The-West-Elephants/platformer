# Import package
from OpenGL.GL import *


class Stone:
    def __init__(self, x, y, width, height, image):
        # Define variables
        self.image = image
        self.direction = 1
        self.rect = {"x": x, "y": y, "width": width, "height": height}
        self.holding = None
        self.throwing = False
        self.forward = 0
        self.jumpCount = 0

    def draw(self):
        # Draw stone
        glBindTexture(GL_TEXTURE_2D, self.image)
        glEnable(GL_TEXTURE_2D)
        glTranslate(self.rect["x"], self.rect["y"], 0)
        glBegin(GL_QUAD_STRIP)
        glTexCoord2f(0, 1)
        glVertex2f(0, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.rect["width"], 0)
        glTexCoord2f(0, 0)
        glVertex2f(0, self.rect["height"])
        glTexCoord2f(1, 0)
        glVertex2f(self.rect["width"], self.rect["height"])
        glEnd()
        glTranslate(-self.rect["x"], -self.rect["y"], 0)
        glDisable(GL_TEXTURE_2D)

    def update(self, tiles):
        # Throwing
        if self.throwing:
            self.rect["x"] += self.forward * self.direction
            self.forward -= 0.002

        # Stop throwing
        if round(self.forward, 5) == 0:
            self.throwing = False
            self.forward = 0

        # Go over player that holding the stone
        if self.holding:
            self.rect["x"] = self.holding.rect["x"]
            self.rect["y"] = self.holding.rect["y"] + self.holding.rect["height"]

        # Gravitation
        if "up" not in self.touchblocks(tiles) and not self.holding:
            self.rect["y"] += self.jumpCount
            self.jumpCount -= 0.001
        elif not self.holding:
            self.rect["y"] += 0.005
            self.jumpCount = 0

        # Change direction
        if "left" in self.touchblocks(tiles) or "right" in self.touchblocks(tiles):
            self.direction *= -1

    def touchblock(self, tile):
        # Check for touch an object
        if (tile.rect["x"] < self.rect["x"] + 0.02 < tile.rect["x"] + tile.rect["width"]) or (self.rect["x"] < tile.rect["x"] + 0.02 < self.rect["x"] + self.rect["width"]) or (self.rect["x"] == tile.rect["x"]):
            if (tile.rect["y"] < self.rect["y"] < tile.rect["y"] + tile.rect["height"]) or (self.rect["y"] < tile.rect["y"] < self.rect["y"] + self.rect["height"]):
                return True
        return False

    def touchblocks(self, tiles):
        # Find directions that stone touch
        touchtiles = []
        touches = []
        for tile in tiles:
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
