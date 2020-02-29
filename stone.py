from OpenGL.GL import *


class Tile:
    def __init__(self, x, y, width, height, image):
        self.image = image
        self.direction = 1
        self.rect = {"x": x, "y": y, "width": width, "height": height}
        self.holding = None
        self.throwing = False
        self.forward = 0

    def draw(self):
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

    def update(self):
        if self.throwing:
            self.rect["x"] += self.forward * self.direction
            self.forward -= 0.001
        if self.holding:
            self.rect["x"] = self.holding.rect["x"]
            self.rect["y"] = self.holding.rect["y"] + self.holding.rect["height"]
