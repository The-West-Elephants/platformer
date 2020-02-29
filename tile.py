# Import package
from OpenGL.GL import *


class Tile:
    def __init__(self, x, y, width, height, color):
        # Define variables
        self.rect = {"x": x, "y": y, "width": width, "height": height}
        self.color = color
        for i in range(len(self.color)):
            self.color[i] = float(self.color[i])

    def draw(self):
        # Draw tile
        glTranslate(self.rect["x"], self.rect["y"], 0)
        glColor3fv(self.color)
        glBegin(GL_QUAD_STRIP)
        glVertex2f(0, 0)
        glVertex2f(self.rect["width"], 0)
        glVertex2f(0, self.rect["height"])
        glVertex2f(self.rect["width"], self.rect["height"])
        glEnd()
        glTranslate(-self.rect["x"], -self.rect["y"], 0)
        glColor3f(1, 1, 1)
